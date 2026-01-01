import { User, AnalysisResult } from './types';

const STORAGE_KEYS = {
  USER: 'bias_detector_user',
  ANALYSES: 'bias_detector_analyses',
};

export const authService = {
  login: (email: string, password: string): User | null => {
    // Mock authentication - in a real app, this would call an API
    const storedUsers = localStorage.getItem('bias_detector_users');
    const users: Array<{ email: string; password: string; name: string; id: string }> = 
      storedUsers ? JSON.parse(storedUsers) : [];
    
    const user = users.find((u) => u.email === email && u.password === password);
    
    if (user) {
      const userData: User = { id: user.id, email: user.email, name: user.name };
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
      return userData;
    }
    
    return null;
  },

  signup: (email: string, password: string, name: string): User | null => {
    const storedUsers = localStorage.getItem('bias_detector_users');
    const users: Array<{ email: string; password: string; name: string; id: string }> = 
      storedUsers ? JSON.parse(storedUsers) : [];
    
    if (users.find((u) => u.email === email)) {
      return null; // User already exists
    }
    
    const newUser = {
      id: `user-${Date.now()}`,
      email,
      password,
      name,
    };
    
    users.push(newUser);
    localStorage.setItem('bias_detector_users', JSON.stringify(users));
    
    const userData: User = { id: newUser.id, email: newUser.email, name: newUser.name };
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
    
    return userData;
  },

  logout: (): void => {
    localStorage.removeItem(STORAGE_KEYS.USER);
  },

  getCurrentUser: (): User | null => {
    const userData = localStorage.getItem(STORAGE_KEYS.USER);
    return userData ? JSON.parse(userData) : null;
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
