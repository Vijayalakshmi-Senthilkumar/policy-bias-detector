export type BiasType = 'gender' | 'age' | 'disability' | 'racial' | 'other';

export type SeverityLevel = 'low' | 'medium' | 'high';

export interface BiasInstance {
  id: string;
  originalText: string;
  biasType: BiasType;
  severity: SeverityLevel;
  explanation: string;
  suggestedRewrite: string;
  startIndex: number;
  endIndex: number;
}

export interface AnalysisResult {
  id: string;
  policyText: string;
  policyName: string;
  analyzedAt: string;
  totalBiasCount: number;
  overallSeverity: SeverityLevel;
  biasInstances: BiasInstance[];
  biasByCategory: Record<BiasType, number>;
}

export interface User {
  id: string;
  email: string;
  name: string;
}
