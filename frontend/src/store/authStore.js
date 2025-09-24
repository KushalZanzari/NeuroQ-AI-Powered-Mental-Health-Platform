import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import api from '../services/api';

const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Actions
      login: async (email, password) => {
        set({ isLoading: true, error: null });
        try {
          const formData = new FormData();
          formData.append('username', email);
          formData.append('password', password);

          const response = await api.post('/api/v1/auth/login', formData, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          });

          const { access_token } = response.data;
          
          // Get user info
          const userResponse = await api.get('/api/v1/auth/me', {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          });

          set({
            user: userResponse.data,
            token: access_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });

          // Set default authorization header
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

          return { success: true };
        } catch (error) {
          const errorMessage = error.response?.data?.detail || 'Login failed';
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });
          return { success: false, error: errorMessage };
        }
      },

      signup: async (userData) => {
        set({ isLoading: true, error: null });
        try {
          const response = await api.post('/api/v1/auth/signup', userData);
          
          set({
            isLoading: false,
            error: null,
          });

          return { success: true, data: response.data };
        } catch (error) {
          const errorMessage = error.response?.data?.detail || 'Signup failed';
          set({
            isLoading: false,
            error: errorMessage,
          });
          return { success: false, error: errorMessage };
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
        });
        
        // Remove authorization header
        delete api.defaults.headers.common['Authorization'];
      },

      updateUser: (userData) => {
        set((state) => ({
          user: { ...state.user, ...userData },
        }));
      },

      setError: (error) => {
        set({ error });
      },

      clearError: () => {
        set({ error: null });
      },

      // Initialize auth state from stored token
      initializeAuth: async () => {
        const { token } = get();
        if (token) {
          set({ isLoading: true });
          try {
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            const response = await api.get('/api/v1/auth/me');
            set({
              user: response.data,
              isAuthenticated: true,
              isLoading: false,
            });
          } catch (error) {
            // Token is invalid, clear auth state
            get().logout();
            set({ isLoading: false });
          }
        } else {
          set({ isLoading: false });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

export default useAuthStore;
export { useAuthStore };
