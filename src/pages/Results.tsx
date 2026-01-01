import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useState } from 'react';
import { Layout } from '@/components/layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AnalysisResult, BiasInstance, BiasType } from '@/lib/types';
import { biasTypeLabels, severityLabels } from '@/lib/mockData';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { ArrowLeft, Download, AlertTriangle, CheckCircle, Copy, Lightbulb } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const biasColors: Record<BiasType, string> = {
  gender: 'hsl(280, 67%, 44%)',
  age: 'hsl(32, 95%, 44%)',
  disability: 'hsl(199, 89%, 48%)',
  racial: 'hsl(0, 72%, 51%)',
  other: 'hsl(220, 9%, 46%)',
};

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const { toast } = useToast();
  const analysis = location.state?.analysis as AnalysisResult | undefined;
  const [selectedBias, setSelectedBias] = useState<BiasInstance | null>(null);

  if (!analysis) {
    return (
      <Layout>
        <div className="container py-20 text-center">
          <h1 className="text-2xl font-bold mb-4">No Analysis Found</h1>
          <Button onClick={() => navigate('/analyze')}>Start New Analysis</Button>
        </div>
      </Layout>
    );
  }

  const chartData = Object.entries(analysis.biasByCategory)
    .filter(([_, count]) => count > 0)
    .map(([type, count]) => ({
      name: biasTypeLabels[type as BiasType],
      count,
      color: biasColors[type as BiasType],
    }));

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-severity-high text-white';
      case 'medium': return 'bg-severity-medium text-white';
      default: return 'bg-severity-low text-white';
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({ title: 'Copied!', description: 'Suggestion copied to clipboard.' });
  };

  const exportPDF = () => {
    toast({ title: 'Export started', description: 'PDF report is being generated...' });
    // In production, this would generate a real PDF
    setTimeout(() => {
      toast({ title: 'PDF Ready', description: 'Your report has been downloaded.' });
    }, 1500);
  };

  return (
    <Layout>
      <div className="container py-8 md:py-12">
        <div className="flex items-center justify-between mb-8">
          <Button variant="ghost" onClick={() => navigate('/analyze')} className="gap-2">
            <ArrowLeft className="h-4 w-4" /> Back
          </Button>
          <Button onClick={exportPDF} className="gap-2">
            <Download className="h-4 w-4" /> Export PDF
          </Button>
        </div>

        <h1 className="text-2xl md:text-3xl font-bold mb-2">{analysis.policyName}</h1>
        <p className="text-muted-foreground mb-8">
          Analyzed on {new Date(analysis.analyzedAt).toLocaleDateString()}
        </p>

        {/* Summary Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Issues</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{analysis.totalBiasCount}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Overall Severity</CardTitle>
            </CardHeader>
            <CardContent>
              <Badge className={getSeverityColor(analysis.overallSeverity)}>
                {severityLabels[analysis.overallSeverity]}
              </Badge>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Categories Affected</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{chartData.length}</div>
            </CardContent>
          </Card>
        </div>

        {/* Chart */}
        {chartData.length > 0 && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Bias by Category</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} layout="vertical">
                    <XAxis type="number" />
                    <YAxis type="category" dataKey="name" width={120} />
                    <Tooltip />
                    <Bar dataKey="count">
                      {chartData.map((entry, index) => (
                        <Cell key={index} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Issues List */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Detected Issues ({analysis.biasInstances.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {analysis.biasInstances.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground flex flex-col items-center gap-2">
                <CheckCircle className="h-8 w-8 text-severity-low" />
                <p>No bias detected in this policy. Great job!</p>
              </div>
            ) : (
              analysis.biasInstances.map((bias) => (
                <div key={bias.id} className="p-4 border border-border rounded-lg">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div>
                      <Badge variant="outline" className="mb-2">{biasTypeLabels[bias.biasType]}</Badge>
                      <Badge className={`ml-2 ${getSeverityColor(bias.severity)}`}>
                        {severityLabels[bias.severity]}
                      </Badge>
                      <p className="font-medium mt-2">"{bias.originalText}"</p>
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground mb-3">{bias.explanation}</p>
                  <div className="flex items-center gap-2 p-3 bg-accent rounded-md">
                    <Lightbulb className="h-4 w-4 text-accent-foreground shrink-0" />
                    <span className="text-sm flex-1">Suggested: <strong>{bias.suggestedRewrite}</strong></span>
                    <Button size="sm" variant="ghost" onClick={() => copyToClipboard(bias.suggestedRewrite)}>
                      <Copy className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
