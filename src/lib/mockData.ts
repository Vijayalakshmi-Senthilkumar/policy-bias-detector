import { AnalysisResult, BiasInstance, BiasType, SeverityLevel } from './types';

export const generateMockAnalysis = (policyText: string, policyName: string): AnalysisResult => {
  const mockBiasPatterns: Array<{
    pattern: RegExp;
    type: BiasType;
    severity: SeverityLevel;
    explanation: string;
    replacement: string;
  }> = [
    {
      pattern: /\bhe\b|\bhis\b|\bhim\b/gi,
      type: 'gender',
      severity: 'medium',
      explanation: 'Using masculine pronouns exclusively can exclude non-male employees and create an unwelcoming environment.',
      replacement: 'they/their/them',
    },
    {
      pattern: /\bmanpower\b/gi,
      type: 'gender',
      severity: 'low',
      explanation: 'The term "manpower" implies that only men contribute to the workforce.',
      replacement: 'workforce or staffing',
    },
    {
      pattern: /\byoung and energetic\b/gi,
      type: 'age',
      severity: 'high',
      explanation: 'Requiring candidates to be "young and energetic" discriminates against older workers and may violate age discrimination laws.',
      replacement: 'motivated and dedicated',
    },
    {
      pattern: /\bdigital native\b/gi,
      type: 'age',
      severity: 'medium',
      explanation: 'The term "digital native" implies preference for younger workers and can discourage qualified older candidates.',
      replacement: 'technologically proficient',
    },
    {
      pattern: /\bphysically fit\b|\bable-bodied\b/gi,
      type: 'disability',
      severity: 'high',
      explanation: 'Requiring physical fitness or being able-bodied may exclude qualified candidates with disabilities who can perform essential job functions.',
      replacement: 'capable of performing essential job functions with or without accommodation',
    },
    {
      pattern: /\bnormal working hours\b/gi,
      type: 'disability',
      severity: 'low',
      explanation: 'The term "normal" can be exclusionary and may not account for reasonable accommodations.',
      replacement: 'standard business hours',
    },
    {
      pattern: /\bcultural fit\b/gi,
      type: 'racial',
      severity: 'medium',
      explanation: '"Cultural fit" can be used to justify discrimination against candidates from different backgrounds.',
      replacement: 'alignment with company values',
    },
    {
      pattern: /\bnative English speaker\b/gi,
      type: 'racial',
      severity: 'high',
      explanation: 'Requiring a "native English speaker" discriminates against equally qualified candidates who learned English as a second language.',
      replacement: 'fluent in English',
    },
  ];

  const biasInstances: BiasInstance[] = [];
  let idCounter = 1;

  mockBiasPatterns.forEach(({ pattern, type, severity, explanation, replacement }) => {
    let match;
    while ((match = pattern.exec(policyText)) !== null) {
      biasInstances.push({
        id: `bias-${idCounter++}`,
        originalText: match[0],
        biasType: type,
        severity,
        explanation,
        suggestedRewrite: replacement,
        startIndex: match.index,
        endIndex: match.index + match[0].length,
      });
    }
  });

  // Sort by position in text
  biasInstances.sort((a, b) => a.startIndex - b.startIndex);

  const biasByCategory: Record<BiasType, number> = {
    gender: 0,
    age: 0,
    disability: 0,
    racial: 0,
    other: 0,
  };

  biasInstances.forEach((instance) => {
    biasByCategory[instance.biasType]++;
  });

  const calculateOverallSeverity = (): SeverityLevel => {
    const highCount = biasInstances.filter((b) => b.severity === 'high').length;
    const mediumCount = biasInstances.filter((b) => b.severity === 'medium').length;
    
    if (highCount > 0) return 'high';
    if (mediumCount > 2) return 'high';
    if (mediumCount > 0) return 'medium';
    return 'low';
  };

  return {
    id: `analysis-${Date.now()}`,
    policyText,
    policyName,
    analyzedAt: new Date().toISOString(),
    totalBiasCount: biasInstances.length,
    overallSeverity: biasInstances.length === 0 ? 'low' : calculateOverallSeverity(),
    biasInstances,
    biasByCategory,
  };
};

export const samplePolicyText = `Employee Conduct Policy

1. Introduction
Every employee must conduct himself in a professional manner during normal working hours. He is expected to represent the company's values and maintain a positive workplace environment.

2. Hiring Standards
We seek young and energetic candidates who are digital natives and can hit the ground running. Applicants must be able-bodied and physically fit to handle the demands of our fast-paced environment.

3. Work Requirements
All manpower resources should be allocated efficiently. Employees must be cultural fit for our team-oriented environment. We prefer native English speakers for client-facing roles.

4. Performance
Each manager should evaluate his team members quarterly. He should provide feedback that helps employees grow in their careers.`;

export const biasTypeLabels: Record<BiasType, string> = {
  gender: 'Gender Bias',
  age: 'Age Bias',
  disability: 'Disability Bias',
  racial: 'Racial/Ethnic Bias',
  other: 'Other Bias',
};

export const severityLabels: Record<SeverityLevel, string> = {
  low: 'Low',
  medium: 'Medium',
  high: 'High',
};
