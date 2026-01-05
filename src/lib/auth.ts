import { User, AnalysisResult } from './types';

const STORAGE_KEYS = {
  USER: 'bias_detector_user',
  TOKEN: 'bias_detector_token',
  ANALYSES: 'bias_detector_analyses',
};

const API_URL = import.meta.env.VITE_API_URL || 'https://policy-bias-detector-backend.onrender.com';

export const authService = {
  login: async (email: string, password: string): Promise<User | null> => {
    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        console.error('Login failed:', response.statusText);
        return null;
      }

      const data = await response.json();
      if (data.success && data.data) {
        const { user, token } = data.data;
        const userData: User = {
          id: user.id,
          email: user.email,
          name: user.name,
          token: token,
        };
        localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
        localStorage.setItem(STORAGE_KEYS.TOKEN, token);
        return userData;
      }

      return null;
    } catch (error) {
      console.error('Login error:', error);
      // Fallback to mock auth if backend is unavailable
      return authService.loginMock(email, password);
    }
  },

  signup: async (email: string, password: string, name: string): Promise<User | null> => {
    try {
      const response = await fetch(`${API_URL}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        console.error('Signup failed:', response.statusText);
        return null;
      }

      const data = await response.json();
      if (data.success && data.data) {
        const { user, token } = data.data;
        const userData: User = {
          id: user.id,
          email: user.email,
          name: user.name,
          token: token,
        };
        localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
        localStorage.setItem(STORAGE_KEYS.TOKEN, token);
        return userData;
      }

      return null;
    } catch (error) {
      console.error('Signup error:', error);
      // Fallback to mock auth if backend is unavailable
      return authService.signupMock(email, password, name);
    }
  },

  // Mock authentication fallbacks
  loginMock: (email: string, password: string): User | null => {
    const storedUsers = localStorage.getItem('bias_detector_users');
    const users: Array<{ email: string; password: string; name: string; id: string }> = 
      storedUsers ? JSON.parse(storedUsers) : [];
    
    const user = users.find((u) => u.email === email && u.password === password);
    
    if (user) {
      const userData: User = {
        id: user.id,
        email: user.email,
        name: user.name,
        token: `mock-token-${Date.now()}`,
      };
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
      return userData;
    }
    
    return null;
  },

  signupMock: (email: string, password: string, name: string): User | null => {
    const storedUsers = localStorage.getItem('bias_detector_users');
    const users: Array<{ email: string; password: string; name: string; id: string }> = 
      storedUsers ? JSON.parse(storedUsers) : [];
    
    if (users.find((u) => u.email === email)) {
      return null;
    }
    
    const newUser = {
      id: `user-${Date.now()}`,
      email,
      password,
      name,
    };
    
    users.push(newUser);
    localStorage.setItem('bias_detector_users', JSON.stringify(users));
    
    const userData: User = {
      id: newUser.id,
      email: newUser.email,
      name: newUser.name,
      token: `mock-token-${Date.now()}`,
    };
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
    
    return userData;
  },

  logout: (): void => {
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
  },

  getCurrentUser: (): User | null => {
    const userData = localStorage.getItem(STORAGE_KEYS.USER);
    return userData ? JSON.parse(userData) : null;
  },

  getToken: (): string | null => {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem(STORAGE_KEYS.USER);
  },
};

export const analysisStorage = {
  save: (analysis: AnalysisResult): void => {
    const user = authService.getCurrentUser();
    if (!user) return;

    const key = `${STORAGE_KEYS.ANALYSES}_${user.id}`;
    const stored = localStorage.getItem(key);
    const analyses: AnalysisResult[] = stored ? JSON.parse(stored) : [];
    
    analyses.unshift(analysis);
    localStorage.setItem(key, JSON.stringify(analyses.slice(0, 50))); // Keep last 50
  },

  getAll: (): AnalysisResult[] => {
    const user = authService.getCurrentUser();
    if (!user) return [];

    const key = `${STORAGE_KEYS.ANALYSES}_${user.id}`;
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : [];
  },

  getById: (id: string): AnalysisResult | null => {
    const analyses = analysisStorage.getAll();
    return analyses.find((a) => a.id === id) || null;
  },

  delete: (id: string): void => {
    const user = authService.getCurrentUser();
    if (!user) return;

    const key = `${STORAGE_KEYS.ANALYSES}_${user.id}`;
    const analyses = analysisStorage.getAll().filter((a) => a.id !== id);
    localStorage.setItem(key, JSON.stringify(analyses));
  },
};
