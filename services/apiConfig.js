/**
 * 热成像 API 配置文件
 * 用于管理 API 服务的地址和相关配置
 */

// API 服务配置
const API_CONFIG = {
  // 开发环境
  development: {
    baseUrl: 'http://localhost:5000',
    apiVersion: 'v1',
    timeout: 300000, // 5分钟
    endpoints: {
      generateReport: '/api/v1/generate-pdf',
      batchGenerate: '/api/v1/batch-generate',
      health: '/health',
      status: '/api/v1/status'
    }
  },
  
  // 生产环境
  production: {
    baseUrl: 'http://your-server:5000', // 需要替换为实际服务器地址
    apiVersion: 'v1',
    timeout: 300000,
    endpoints: {
      generateReport: '/api/v1/generate-pdf',
      batchGenerate: '/api/v1/batch-generate',
      health: '/health',
      status: '/api/v1/status'
    }
  }
};

/**
 * 获取当前环境的 API 配置
 * @returns {Object} API 配置对象
 */
export function getApiConfig() {
  // 判断是否为生产环境
  // 可以根据 URL、环境变量等进行判断
  const isDev = process.env.NODE_ENV === 'development' || 
                location.hostname === 'localhost' ||
                location.hostname === '127.0.0.1';
  
  return isDev ? API_CONFIG.development : API_CONFIG.production;
}

/**
 * 获取完整的 API 端点 URL
 * @param {string} endpoint - 端点名称 (e.g., 'generateReport')
 * @returns {string} 完整的 URL
 */
export function getApiUrl(endpoint) {
  const config = getApiConfig();
  const path = config.endpoints[endpoint];
  
  if (!path) {
    throw new Error(`未知的 API 端点: ${endpoint}`);
  }
  
  return `${config.baseUrl}${path}`;
}

/**
 * 获取 API 基础 URL
 * @returns {string} 基础 URL
 */
export function getBaseUrl() {
  return getApiConfig().baseUrl;
}

/**
 * 获取 API 超时时间
 * @returns {number} 超时时间（毫秒）
 */
export function getApiTimeout() {
  return getApiConfig().timeout;
}

/**
 * 检查 API 服务是否可用
 * @returns {Promise<boolean>} 是否可用
 */
export async function checkApiHealth() {
  try {
    const response = await uni.request({
      url: getApiUrl('health'),
      method: 'GET',
      timeout: 5000 // 使用较短的超时时间进行健康检查
    });
    
    return response.statusCode === 200;
  } catch (error) {
    console.error('API 健康检查失败:', error);
    return false;
  }
}

/**
 * 获取 API 状态信息
 * @returns {Promise<Object|null>} API 状态对象或 null
 */
export async function getApiStatus() {
  try {
    const response = await uni.request({
      url: getApiUrl('status'),
      method: 'GET',
      timeout: 5000
    });
    
    if (response.statusCode === 200) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('获取 API 状态失败:', error);
    return null;
  }
}

// 导出所有配置
export default {
  API_CONFIG,
  getApiConfig,
  getApiUrl,
  getBaseUrl,
  getApiTimeout,
  checkApiHealth,
  getApiStatus
};
