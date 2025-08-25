// 路线导入器 Web应用 - 主要JavaScript逻辑
class RouteImporter {
    constructor() {
        this.currentRoute = null;
        this.map = null;
        this.markers = [];
        this.routePolyline = null;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initMap();
    }
    
    bindEvents() {
        // 解析按钮点击事件
        document.getElementById('parseBtn').addEventListener('click', () => {
            this.parseNote();
        });
        
        // 在地图App中打开按钮
        document.getElementById('openInMapsBtn').addEventListener('click', () => {
            this.openInMaps();
        });
        
        // 保存路线按钮
        document.getElementById('saveRouteBtn').addEventListener('click', () => {
            this.showSaveModal();
        });
        
        // 保存弹窗相关事件
        document.getElementById('closeModalBtn').addEventListener('click', () => {
            this.hideSaveModal();
        });
        
        document.getElementById('cancelSaveBtn').addEventListener('click', () => {
            this.hideSaveModal();
        });
        
        document.getElementById('confirmSaveBtn').addEventListener('click', () => {
            this.saveRoute();
        });
        
        // 重试按钮
        document.getElementById('retryBtn').addEventListener('click', () => {
            this.parseNote();
        });
        
        // 定位按钮
        document.getElementById('centerMapBtn').addEventListener('click', () => {
            this.centerMap();
        });
        
        // 回车键触发解析
        document.getElementById('noteUrl').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.parseNote();
            }
        });
    }
    
    async parseNote() {
        const url = document.getElementById('noteUrl').value.trim();
        
        if (!url) {
            this.showError('请输入小红书笔记链接');
            return;
        }
        
        if (!this.isValidUrl(url)) {
            this.showError('请输入有效的小红书链接');
            return;
        }
        
        this.showLoading();
        this.hideError();
        
        try {
            const response = await fetch('/api/parse-note', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.currentRoute = result.data;
                this.showResult();
                this.displayRoute();
            } else {
                throw new Error(result.error || '解析失败');
            }
            
        } catch (error) {
            console.error('解析失败:', error);
            this.showError(error.message || '解析失败，请重试');
        } finally {
            this.hideLoading();
        }
    }
    
    isValidUrl(url) {
        return url.includes('xiaohongshu.com') || url.includes('xhslink.com');
    }
    
    showLoading() {
        document.getElementById('loadingSection').style.display = 'block';
        document.getElementById('inputSection').style.display = 'none';
        document.getElementById('resultSection').style.display = 'none';
        document.getElementById('errorSection').style.display = 'none';
    }
    
    hideLoading() {
        document.getElementById('loadingSection').style.display = 'none';
    }
    
    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorSection').style.display = 'block';
        document.getElementById('inputSection').style.display = 'block';
        document.getElementById('resultSection').style.display = 'none';
    }
    
    hideError() {
        document.getElementById('errorSection').style.display = 'none';
    }
    
    showResult() {
        document.getElementById('inputSection').style.display = 'none';
        document.getElementById('resultSection').style.display = 'block';
        document.getElementById('errorSection').style.display = 'none';
    }
    
    displayRoute() {
        if (!this.currentRoute) return;
        
        // 更新路线信息
        this.updateRouteInfo();
        
        // 在地图上显示路线
        this.displayRouteOnMap();
    }
    
    updateRouteInfo() {
        const route = this.currentRoute;
        
        // 更新标题
        document.getElementById('routeTitle').textContent = route.title || '未命名路线';
        
        // 更新距离和时间
        if (route.estimatedDistance) {
            document.getElementById('routeDistance').textContent = `距离: ${route.estimatedDistance.toFixed(1)}公里`;
        }
        
        if (route.estimatedDuration) {
            const hours = Math.floor(route.estimatedDuration / 60);
            const minutes = route.estimatedDuration % 60;
            let durationText = '';
            if (hours > 0) {
                durationText = `${hours}小时${minutes}分钟`;
            } else {
                durationText = `${minutes}分钟`;
            }
            document.getElementById('routeDuration').textContent = `时间: ${durationText}`;
        }
        
        // 更新地点列表
        this.updatePlacesList(route.places);
    }
    
    updatePlacesList(places) {
        const placesList = document.getElementById('placesList');
        placesList.innerHTML = '';
        
        places.forEach((place, index) => {
            const placeItem = document.createElement('div');
            placeItem.className = 'place-item';
            
            const placeNumber = document.createElement('div');
            placeNumber.className = 'place-number';
            placeNumber.textContent = index + 1;
            
            const placeInfo = document.createElement('div');
            placeInfo.className = 'place-info';
            
            const placeName = document.createElement('div');
            placeName.className = 'place-name';
            placeName.textContent = place.name;
            
            const placeAddress = document.createElement('div');
            placeAddress.className = 'place-address';
            placeAddress.textContent = place.address || '地址信息';
            
            placeInfo.appendChild(placeName);
            placeInfo.appendChild(placeAddress);
            
            placeItem.appendChild(placeNumber);
            placeItem.appendChild(placeInfo);
            
            placesList.appendChild(placeItem);
        });
    }
    
    initMap() {
        // 初始化地图（这里使用简单的占位符，实际项目中可以集成Google Maps或其他地图服务）
        const mapElement = document.getElementById('map');
        
        // 创建简单的地图占位符
        const mapPlaceholder = document.createElement('div');
        mapPlaceholder.style.cssText = `
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #f0f0f0 25%, transparent 25%), 
                        linear-gradient(-45deg, #f0f0f0 25%, transparent 25%), 
                        linear-gradient(45deg, transparent 75%, #f0f0f0 75%), 
                        linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #666;
            font-size: 1.2rem;
            text-align: center;
            padding: 2rem;
        `;
        mapPlaceholder.innerHTML = `
            <div>
                <div style="font-size: 3rem; margin-bottom: 1rem;">🗺️</div>
                <div>路线地图</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.7;">
                    点击"在地图App中打开"查看完整路线
                </div>
            </div>
        `;
        
        mapElement.appendChild(mapPlaceholder);
    }
    
    displayRouteOnMap() {
        // 这里可以集成真正的地图服务来显示路线
        // 目前使用占位符，实际项目中可以：
        // 1. 集成Google Maps JavaScript API
        // 2. 显示路线点和连线
        // 3. 添加路线信息窗口
        console.log('显示路线:', this.currentRoute);
    }
    
    openInMaps() {
        if (!this.currentRoute) return;
        
        // 生成Google Maps导航链接
        const gmapsUrl = this.generateGoogleMapsUrl();
        
        if (gmapsUrl) {
            // 在新窗口中打开Google Maps
            window.open(gmapsUrl, '_blank');
        } else {
            this.showToast('无法生成地图链接');
        }
    }
    
    generateGoogleMapsUrl() {
        if (!this.currentRoute || !this.currentRoute.places || this.currentRoute.places.length < 2) {
            return null;
        }
        
        const places = this.currentRoute.places;
        
        // 起点
        const origin = encodeURIComponent(places[0].address || places[0].name);
        
        // 终点（环形路线回到起点）
        const destination = encodeURIComponent(places[0].address || places[0].name);
        
        // 途经点
        const waypoints = places.slice(1).map(place => 
            encodeURIComponent(place.address || place.name)
        ).join('/');
        
        // 构建Google Maps导航链接
        let url = `https://www.google.com/maps/dir/${origin}`;
        if (waypoints) {
            url += `/${waypoints}`;
        }
        url += `/${destination}/data=!4m2!4m1!3e2`;
        
        return url;
    }
    
    showSaveModal() {
        if (!this.currentRoute) return;
        
        // 预填充路线名称
        document.getElementById('routeName').value = this.currentRoute.title || '未命名路线';
        document.getElementById('routeDescription').value = this.currentRoute.content || '';
        
        document.getElementById('saveModal').style.display = 'flex';
    }
    
    hideSaveModal() {
        document.getElementById('saveModal').style.display = 'none';
    }
    
    async saveRoute() {
        const routeName = document.getElementById('routeName').value.trim();
        const routeDescription = document.getElementById('routeDescription').value.trim();
        
        if (!routeName) {
            this.showToast('请输入路线名称');
            return;
        }
        
        try {
            const response = await fetch('/api/save-route', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: routeName,
                    description: routeDescription
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showToast('路线保存成功！');
                this.hideSaveModal();
            } else {
                throw new Error(result.error || '保存失败');
            }
            
        } catch (error) {
            console.error('保存失败:', error);
            this.showToast(error.message || '保存失败，请重试');
        }
    }
    
    centerMap() {
        // 居中显示地图（实际项目中可以定位到用户当前位置或路线中心）
        this.showToast('地图已居中');
    }
    
    showToast(message) {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toastMessage');
        
        toastMessage.textContent = message;
        toast.style.display = 'block';
        
        // 3秒后自动隐藏
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new RouteImporter();
});
