import { useNavigate } from 'react-router-dom';
import { Layout } from '@/components/layout';
import { Button } from '@/components/ui/button';
import { generateMockAnalysis, samplePolicyText } from '@/lib/mockData';
import { ArrowRight } from 'lucide-react';

export default function Demo() {
  const navigate = useNavigate();

  const handleViewDemo = () => {
    const analysis = generateMockAnalysis(samplePolicyText, 'Sample Employee Conduct Policy');
    navigate(`/results/${analysis.id}`, { state: { analysis } });
  };

  return (
    <Layout>
      <div className="container py-20 text-center">
        <h1 className="text-3xl md:text-4xl font-bold mb-4">See PolicyGuard AI in Action</h1>
        <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
          We'll analyze a sample employee policy to show you how our AI detects and explains hidden bias.
        </p>
        <Button size="lg" onClick={handleViewDemo} className="gap-2">
          Run Demo Analysis
          <ArrowRight className="h-4 w-4" />
        </Button>
      </div>
    </Layout>
  );
}
