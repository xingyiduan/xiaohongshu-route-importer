// 集成火山引擎豆包API的前端JavaScript

// 全局变量
let currentParsedNote = null;
let currentPlannedRoute = null;

// DOM元素
const urlInput = document.getElementById('url-input');
const parseBtn = document.getElementById('parse-btn');
const resultSection = document.getElementById('result-section');
const loadingSection = document.getElementById('loading-section');
const errorSection = document.getElementById('error-section');
const routeInfoCard = document.getElementById('route-info-card');
const placesList = document.getElementById('places-list');
const mapSection = document.getElementById('map-section');
const openMapBtn = document.getElementById('open-map-btn');
const saveRouteBtn = document.getElementById('save-route-btn');
const saveModal = document.getElementById('save-modal');
const saveForm = document.getElementById('save-form');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 绑定事件
    parseBtn.addEventListener('click', parseNote);
    openMapBtn.addEventListener('click', openInMap);
    saveRouteBtn.addEventListener('click', showSaveModal);
    saveForm.addEventListener('click', saveRoute);
    
    // 关闭模态框
    document.querySelectorAll('.close').forEach(btn => {
        btn.addEventListener('click', () => {
            saveModal.style.display = 'none';
            document.getElementById('map-select-modal').style.display = 'none';
        });
    });
    
    // 点击模态框外部关闭
    window.addEventListener('click', (e) => {
        if (e.target === saveModal) {
            saveModal.style.display = 'none';
        }
        if (e.target === document.getElementById('map-select-modal')) {
            document.getElementById('map-select-modal').style.display = 'none';
        }
    });
});

// 提取链接函数
function extractUrl(inputText) {
    // 匹配小红书链接的正则表达式
    const urlPatterns = [
        /https?:\/\/xhslink\.com\/m\/[a-zA-Z0-9]+/g,  // xhslink.com/m/格式
        /https?:\/\/xhslink\.com\/[^\s]+/g,           // 其他xhslink格式
        /https?:\/\/www\.xiaohongshu\.com\/[^\s]+/g,  // xiaohongshu.com格式
        /https?:\/\/[^\s]*xiaohongshu[^\s]*/g,        // 包含xiaohongshu的链接
        /https?:\/\/[^\s]*xhslink[^\s]*/g             // 包含xhslink的链接
    ];
    
    let extractedUrl = null;
    
    // 遍历所有正则表达式模式
    for (const pattern of urlPatterns) {
        const matches = inputText.match(pattern);
        if (matches && matches.length > 0) {
            // 选择第一个匹配的链接
            extractedUrl = matches[0];
            
            // 清理链接，移除可能的尾随字符
            extractedUrl = extractedUrl.replace(/[^\w\-\.\/\?\=\&\#]+$/, '');
            break;
        }
    }
    
    // 如果没有找到链接，尝试查找可能的链接片段
    if (!extractedUrl) {
        // 查找可能的链接片段
        const linkFragments = inputText.match(/[a-zA-Z0-9]{8,}/g);
        if (linkFragments) {
            // 如果找到类似链接ID的片段，提示用户
            console.log('找到可能的链接片段:', linkFragments);
        }
    }
    
    return extractedUrl;
}

// 解析笔记
async function parseNote() {
    const inputText = urlInput.value.trim();
    
    if (!inputText) {
        showError('请输入小红书链接或包含链接的文本');
        return;
    }
    
    // 提取链接
    const extractedUrl = extractUrl(inputText);
    
    if (!extractedUrl) {
        showError('未找到有效的小红书链接，请检查输入内容');
        return;
    }
    
    // 显示提取到的链接（调试信息）
    console.log('提取到的链接:', extractedUrl);
    
    // 显示加载状态
    showLoading('正在使用AI解析小红书笔记...');
    
    try {
        const response = await fetch('/api/parse-note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: extractedUrl })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentParsedNote = result.data;
            showResult(result.data);
            showSuccess(result.message);
        } else {
            showError(result.error || '解析失败');
        }
        
    } catch (error) {
        console.error('解析失败:', error);
        showError('网络错误，请重试');
    }
}

// 规划路线
async function planRoute() {
    if (!currentParsedNote) {
        showError('请先解析笔记');
        return;
    }
    
    showLoading('正在规划步行路线...');
    
    try {
        const response = await fetch('/api/plan-route', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentPlannedRoute = result.data;
            updateRouteInfo(result.data);
            showSuccess(result.message);
        } else {
            showError(result.error || '路线规划失败');
        }
        
    } catch (error) {
        console.error('路线规划失败:', error);
        showError('网络错误，请重试');
    }
}

// 显示结果
function showResult(data) {
    // 更新路线信息
    updateRouteInfo(data);
    
    // 更新多路线展示
    updateRoutesList(data.routes || []);
    
    // 更新地点列表（汇总所有路线的地点）
    const allPlaces = getAllPlacesFromRoutes(data.routes || []);
    updatePlacesList(allPlaces);
    
    // 显示结果区域
    resultSection.style.display = 'block';
    loadingSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // 自动规划路线 - 已禁用，避免页面卡顿
    // planRoute();
}

// 更新路线信息
function updateRouteInfo(data) {
    const title = data.title || '未命名路线';
    const content = data.content || '';
    const tags = data.tags || [];
    
    routeInfoCard.innerHTML = `
        <h3>${title}</h3>
        <p class="description">${content}</p>
        <div class="tags">
            ${tags.map(tag => `<span class="tag">#${tag}</span>`).join('')}
        </div>
    `;
}

// 更新多路线展示
function updateRoutesList(routes) {
    const routesListElement = document.getElementById('routes-list');
    if (!routesListElement) return;
    
    // 安全检查：确保routes存在且是数组
    if (!routes || !Array.isArray(routes) || routes.length === 0) {
        routesListElement.innerHTML = '<p class="no-routes">未找到路线信息</p>';
        return;
    }
    
    const routesHtml = routes.map((route, routeIndex) => {
        // 安全检查：确保route和route.places存在
        if (!route || !route.places || !Array.isArray(route.places)) {
            return '';
        }
        
        return `
        <div class="route-card" data-route-id="${route.route_id || `route_${routeIndex + 1}`}">
            <div class="route-header">
                <h4 class="route-title">${route.route_name || `路线${routeIndex + 1}`}</h4>
                <p class="route-description">${route.route_description || ''}</p>
            </div>
            
            <div class="route-places">
                <h5>📍 路线地点 (${route.places.length}个)</h5>
                <div class="route-places-list">
                    ${route.places.map((place, placeIndex) => {
                        if (!place || !place.name) return '';
                        return `
                        <div class="route-place-item">
                            <div class="place-order">${place.order || placeIndex + 1}</div>
                            <div class="place-details">
                                <span class="place-name">
                                    ${place.name}
                                    ${place.city ? `<span class="city-label">[${place.city}]</span>` : ''}
                                </span>
                                <span class="place-category">${getCategoryName(place.category)}</span>
                            </div>
                        </div>
                        `;
                    }).join('')}
                </div>
            </div>
            
            <div class="route-actions">
                <button class="btn btn-secondary btn-sm" onclick="openRouteInMap('${route.route_id || `route_${routeIndex + 1}`}')">
                    <span class="btn-icon">🗺️</span>
                    路线导航
                </button>
                <button class="btn btn-success btn-sm" onclick="saveRoute('${route.route_id || `route_${routeIndex + 1}`}')">
                    <span class="btn-icon">💾</span>
                    保存路线
                </button>
            </div>
        </div>
        `;
    }).join('');
    
    routesListElement.innerHTML = routesHtml;
}

// 获取所有路线的地点汇总
function getAllPlacesFromRoutes(routes) {
    const allPlaces = [];
    const seenPlaces = new Set();
    
    // 安全检查：确保routes存在且是数组
    if (!routes || !Array.isArray(routes)) {
        return allPlaces;
    }
    
    routes.forEach(route => {
        if (route && route.places && Array.isArray(route.places)) {
            route.places.forEach(place => {
                if (place && place.name) {
                    const placeKey = place.name.toLowerCase();
                    if (!seenPlaces.has(placeKey)) {
                        seenPlaces.add(placeKey);
                        allPlaces.push({
                            ...place,
                            route_source: route.route_name
                        });
                    }
                }
            });
        }
    });
    
    return allPlaces;
}

// 更新地点列表
function updatePlacesList(places) {
    if (!places || !Array.isArray(places) || places.length === 0) {
        placesList.innerHTML = '<p class="no-places">未找到地点信息</p>';
        return;
    }
    
    const placesHtml = places.map((place, index) => {
        // 安全检查：确保place和place.name存在
        if (!place || !place.name) {
            return '';
        }
        
        return `
        <div class="place-item">
            <div class="place-number">${index + 1}</div>
            <div class="place-info">
                <h4 class="place-name">
                    ${place.name}
                    ${place.city ? `<span class="city-label">[${place.city}]</span>` : ''}
                    ${place.alternative_name ? `<span class="alt-name">(${place.alternative_name})</span>` : ''}
                </h4>
                <p class="place-description">${place.description || ''}</p>
                <div class="place-meta">
                    <span class="place-category">${getCategoryName(place.category)}</span>
                    ${place.region ? `<span class="region-label">📍 ${place.region}</span>` : ''}
                    ${place.address ? `<span class="place-address">📍 ${place.address}</span>` : ''}
                    ${place.route_source ? `<span class="route-source">🗺️ ${place.route_source}</span>` : ''}
                </div>
            </div>
        </div>
        `;
    }).join('');
    
    placesList.innerHTML = placesHtml;
}

// 获取类别名称
function getCategoryName(category) {
    const categoryNames = {
        'transportation': '🚉 交通',
        'attraction': '🏛️ 景点',
        'shopping': '🛍️ 购物',
        'restaurant': '🍽️ 餐厅',
        'park': '🌳 公园',
        'other': '📍 其他'
    };
    return categoryNames[category] || '📍 其他';
}

// 在地图应用中打开
function openInMap() {
    // 显示地图选择模态框
    document.getElementById('map-select-modal').style.display = 'none';
}

// 在Google Maps中打开
function openInGoogleMaps() {
    if (!currentParsedNote) {
        showError('请先解析笔记');
        return;
    }
    
    // 获取所有地点
    let places = [];
    if (currentParsedNote.routes && currentParsedNote.routes.length > 0) {
        // 多路线：收集所有路线的地点
        currentParsedNote.routes.forEach(route => {
            if (route.places && Array.isArray(route.places)) {
                places = places.concat(route.places);
            }
        });
    } else if (currentParsedNote.places) {
        // 单路线：直接使用地点列表
        places = currentParsedNote.places;
    }
    
    if (places.length === 0) {
        showError('没有地点信息');
        return;
    }
    
    // 构建Google Maps URL
    const origin = places[0].address || places[0].name;
    const destination = places[places.length - 1].address || places[places.length - 1].name;
    const waypoints = places.slice(1, -1).map(place => place.address || place.name);
    
    let mapsUrl = `https://www.google.com/maps/dir/${encodeURIComponent(origin)}`;
    if (waypoints.length > 0) {
        mapsUrl += `/${waypoints.map(wp => encodeURIComponent(wp)).join('/')}`;
    }
    mapsUrl += `/${encodeURIComponent(destination)}/data=!4m2!4m1!3e2`;
    
    // 关闭模态框
    document.getElementById('map-select-modal').style.display = 'none';
    
    // 打开Google Maps
    window.open(mapsUrl, '_blank');
}

// 打开特定路线在地图应用中
function openRouteInMap(routeId) {
    if (!currentParsedNote || !currentParsedNote.routes) {
        showError('没有路线信息');
        return;
    }
    
    const route = currentParsedNote.routes.find(r => r.route_id === routeId);
    if (!route || !route.places || route.places.length === 0) {
        showError('路线信息不完整');
        return;
    }
    
    const places = route.places;
    const origin = places[0].address || places[0].name;
    const destination = places[places.length - 1].address || places[places.length - 1].name;
    const waypoints = places.slice(1, -1).map(place => place.address || place.name);
    
    let mapsUrl = `https://www.google.com/maps/dir/${encodeURIComponent(origin)}`;
    if (waypoints.length > 0) {
        mapsUrl += `/${waypoints.map(wp => encodeURIComponent(wp)).join('/')}`;
    }
    mapsUrl += `/${encodeURIComponent(destination)}/data=!4m2!4m1!3e2`;
    
    // 打开Google Maps
    window.open(mapsUrl, '_blank');
}

// 显示保存路线模态框
function showSaveModal() {
    // 功能开发中提示
    showInfo('💡 保存路线功能正在开发中，敬请期待！');
}

// 保存路线
async function saveRoute() {
    const formData = new FormData(saveForm);
    const data = {
        name: formData.get('name'),
        description: formData.get('description'),
        source_url: formData.get('source_url')
    };
    
    try {
        const response = await fetch('/api/save-route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess('路线保存成功！');
            saveModal.style.display = 'none';
            saveForm.reset();
        } else {
            showError(result.error || '保存失败');
        }
        
    } catch (error) {
        console.error('保存失败:', error);
        showError('网络错误，请重试');
    }
}

// 显示加载状态
function showLoading(message) {
    loadingSection.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
    loadingSection.style.display = 'block';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// 显示成功消息
function showSuccess(message) {
    // 这里可以添加成功提示，比如toast通知
    console.log('成功:', message);
}

// 显示错误提示
function showError(message) {
    errorSection.style.display = 'block';
    loadingSection.style.display = 'none';
    resultSection.style.display = 'none';
    
    const errorMessage = document.getElementById('error-message');
    if (errorMessage) {
        errorMessage.textContent = message;
    }
}

// 显示信息提示
function showInfo(message) {
    // 创建临时提示元素
    const infoToast = document.createElement('div');
    infoToast.className = 'info-toast';
    infoToast.innerHTML = `
        <div class="info-content">
            <span class="info-icon">💡</span>
            <p>${message}</p>
        </div>
    `;
    
    // 添加到页面
    document.body.appendChild(infoToast);
    
    // 显示动画
    setTimeout(() => {
        infoToast.classList.add('show');
    }, 100);
    
    // 3秒后自动隐藏
    setTimeout(() => {
        infoToast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(infoToast);
        }, 300);
    }, 3000);
}

// 保存特定路线
async function saveRoute(routeId) {
    if (!currentParsedNote || !currentParsedNote.routes) {
        showError('没有路线信息');
        return;
    }
    
    const route = currentParsedNote.routes.find(r => r.route_id === routeId);
    if (!route) {
        showError('路线不存在');
        return;
    }
    
    // 预填充表单
    document.getElementById('route-name').value = route.route_name || '未命名路线';
    document.getElementById('route-description').value = route.route_description || '';
    document.getElementById('source-url').value = urlInput.value;
    
    // 存储当前要保存的路线信息
    window.currentRouteToSave = route;
    
    saveModal.style.display = 'block';
}
