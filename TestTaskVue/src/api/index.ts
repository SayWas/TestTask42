import axios from 'axios';
import router from '../router';
import { useUserStore } from '../stores/userStore';

const loginConfig = {
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'multipart/form-data'
  },
  withCredentials: true
};

export const LoginAPIInstance = axios.create(loginConfig);

const defaultConfig = {
  baseURL: "http://localhost:8000/api",
  headers:{
    'Content-Type': 'application/json'
  }
};

export const DefaultAPIInstance = axios.create(defaultConfig);

DefaultAPIInstance.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const userStore = useUserStore();

      try {
        await userStore.refreshToken();
        originalRequest.headers['Authorization'] = `Bearer ${userStore.userAccessToken}`;
        return DefaultAPIInstance(originalRequest);
      } catch (refreshError) {
        const redirectPath = router.currentRoute.value.fullPath;
        await router.push({ name: 'login', query: { redirect: redirectPath } });
      }
    }
    return Promise.reject(error);
  }
);
