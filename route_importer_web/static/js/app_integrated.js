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
const parserInfoSection = document.getElementById('parser-info-section');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 获取解析器信息
    getParserInfo();
    
    // 绑定事件
    parseBtn.addEventListener('click', parseNote);
    openMapBtn.addEventListener('click', openInMap);
    saveRouteBtn.addEventListener('click', showSaveModal);
    saveForm.addEventListener('click', saveRoute);
    
    // 关闭模态框
    document.querySelectorAll('.close').forEach(btn => {
        btn.addEventListener('click', () => {
            saveModal.style.display = 'none';
        });
    });
    
    // 点击模态框外部关闭
    window.addEventListener('click', (e) => {
        if (e.target === saveModal) {
            saveModal.style.display = 'none';
        }
    });
});

// 获取解析器信息
async function getParserInfo() {
    try {
        const response = await fetch('/api/parser-info');
        const result = await response.json();
        
        if (result.success) {
            displayParserInfo(result.data);
        }
    } catch (error) {
        console.error('获取解析器信息失败:', error);
    }
}

// 显示解析器信息
function displayParserInfo(info) {
    const html = `
        <div class="parser-info">
            <h3>🤖 解析器状态</h3>
            <div class="info-grid">
                <div class="info-item">
                    <span class="label">主要解析器:</span>
                    <span class="value">${info.primary_parser === 'volcengine_douban' ? '火山引擎豆包AI' : '规则解析器'}</span>
                </div>
                <div class="info-item">
                    <span class="label">AI解析器:</span>
                    <span class="value ${info.volcengine_available ? 'success' : 'error'}">${info.volcengine_available ? '可用' : '失败'}</span>
                </div>
                <div class="info-item">
                    <span class="label">回退机制:</span>
                    <span class="value">${info.fallback_enabled ? '启用' : '禁用'}</span>
                </div>
                <div class="info-item">
                    <span class="label">策略:</span>
                    <span class="value">${info.strategy === 'ai_first_with_fallback' ? 'AI优先+回退' : '仅规则'}</span>
                </div>
            </div>
            ${info.volcengine_available && info.volcengine_usage ? `
            <div class="usage-info">
                <h4>📊 API使用统计</h4>
                <div class="usage-grid">
                    <div class="info-item">
                        <span class="label">今日已调用:</span>
                        <span class="value">${info.volcengine_usage.today_calls}/${info.volcengine_usage.max_daily_calls}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">剩余次数:</span>
                        <span class="value">${info.volcengine_usage.remaining_daily}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">每分钟限制:</span>
                        <span class="value">${info.volcengine_usage.minute_calls}/${info.volcengine_usage.max_minute_calls}</span>
                    </div>
                </div>
            </div>
            ` : ''}
        </div>
    `;
    
    parserInfoSection.innerHTML = html;
}

// 解析笔记
async function parseNote() {
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('请输入小红书链接');
        return;
    }
    
    // 显示加载状态
    showLoading('正在使用AI解析小红书笔记...');
    
    try {
        const response = await fetch('/api/parse-note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
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
    
    // 更新地点列表
    updatePlacesList(data.places || []);
    
    // 显示结果区域
    resultSection.style.display = 'block';
    loadingSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // 自动规划路线
    planRoute();
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

// 更新地点列表
function updatePlacesList(places) {
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="no-places">未找到地点信息</p>';
        return;
    }
    
    const placesHtml = places.map((place, index) => `
        <div class="place-item">
            <div class="place-number">${index + 1}</div>
            <div class="place-info">
                <h4 class="place-name">${place.name}</h4>
                <p class="place-description">${place.description || ''}</p>
                <div class="place-meta">
                    <span class="place-category">${getCategoryName(place.category)}</span>
                    ${place.address ? `<span class="place-address">📍 ${place.address}</span>` : ''}
                </div>
            </div>
        </div>
    `).join('');
    
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
    if (!currentPlannedRoute || !currentParsedNote) {
        showError('请先完成路线规划');
        return;
    }
    
    const places = currentParsedNote.places || [];
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
    
    // 打开Google Maps
    window.open(mapsUrl, '_blank');
}

// 显示保存模态框
function showSaveModal() {
    if (!currentPlannedRoute || !currentParsedNote) {
        showError('请先完成路线规划');
        return;
    }
    
    // 预填充表单
    document.getElementById('route-name').value = currentParsedNote.title || '未命名路线';
    document.getElementById('route-description').value = currentParsedNote.content || '';
    document.getElementById('source-url').value = urlInput.value;
    
    saveModal.style.display = 'block';
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

// 显示错误消息
function showError(message) {
    errorSection.innerHTML = `
        <div class="error">
            <p>❌ ${message}</p>
        </div>
    `;
    errorSection.style.display = 'block';
    loadingSection.style.display = 'none';
}
