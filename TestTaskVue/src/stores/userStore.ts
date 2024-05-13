import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { AuthAPI } from '../api/auth-api'
import type { TokenResponse } from '../api/auth-api'

export const useUserStore = defineStore('user', () => {
  const userAccessToken = ref('')
  const userRefreshToken = ref('')

  const isAuthenticated = computed(() => userAccessToken.value !== '');

  const login = async (email: string, password: string): Promise<void> => {
    try {
      const tokens: TokenResponse = await AuthAPI.get_token(email, password);
      userAccessToken.value = tokens.accessToken;
      userRefreshToken.value = tokens.refreshToken;
    } catch (error) {
      console.error('Login failed:', error);
      throw new Error('Login failed');
    }
  };

  const refreshToken = async (): Promise<void> => {
    try {
      if (userRefreshToken.value === '') {
        throw new Error('Refresh token is not available.');
      }
      const newAccessToken: string = await AuthAPI.refresh_token(userRefreshToken.value);
      userAccessToken.value = newAccessToken;
    } catch (error) {
      console.error('Refresh token failed:', error);
      throw new Error('Failed to refresh token');
    }
  };

  return {
    userAccessToken,
    userRefreshToken,
    isAuthenticated,
    login,
    refreshToken
  }
})

interface userSchema {
  id: number
  email: string
  firstName: string
  lastName: string
}

export type { userSchema }
