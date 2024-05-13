import { LoginAPIInstance } from '@/api'

export interface TokenResponse {
  accessToken: string;
  refreshToken: string;
}

export const AuthAPI = {
  /**
   * Authenticates user and retrieves the access token and refresh token.
   * @param email - The user's email address.
   * @param password - The user's password.
   * @returns A Promise resolving to an object containing both the access and refresh tokens.
   * @throws Will throw an error if the login request fails or if the expected tokens are not received.
   */
  async get_token(email: string, password: string): Promise<TokenResponse> {
    const url: string = '/token/';
    const formData: FormData = new FormData();
    formData.set('username', email);
    formData.set('password', password);

    try {
      const response = await LoginAPIInstance.post(url, formData);
      if (response.status === 200 && response.data?.access && response.data?.refresh) {
        const tokens: TokenResponse = {
          accessToken: response.data.access,
          refreshToken: response.data.refresh
        };
        return tokens;
      } else {
        throw new Error(`Unexpected response format or status code: ${response.status}`);
      }
    } catch (error) {
      console.error('Login error:', error);
      throw new Error('Error occurred while logging in');
    }
  },

  /**
   * Refreshes the authentication token using the refresh token provided.
   * @param refreshToken - The refresh token used to obtain a new access token.
   * @returns A Promise resolving to the new access token.
   * @throws Will throw an error if the token refresh fails.
   */
  async refresh_token(refreshToken: string): Promise<string> {
    const url = '/token/refresh/';
    const formData = new FormData();
    formData.set('refresh', refreshToken);

    try {
      const response = await LoginAPIInstance.post(url, formData);
      if (response.status === 200 && response.data?.access) {
        return response.data.access;
      } else {
        throw new Error(`Unexpected response format or status code: ${response.status}`);
      }
    } catch (error) {
      console.error('Token refresh error:', error);
      throw new Error('Error occurred while refreshing token');
    }
  }
}
