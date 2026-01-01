import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Layout } from '@/components/layout';
import { 
  Shield, 
  Search, 
  FileText, 
  CheckCircle, 
  ArrowRight,
  AlertTriangle,
  Lightbulb,
  BarChart3,
  Users,
  Scale,
  Building2
} from 'lucide-react';

export default function Index() {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="py-20 md:py-32 bg-gradient-to-b from-accent/50 to-background">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6">
              <Shield className="h-4 w-4" />
              Enterprise-Ready AI Solution
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6 tracking-tight">
              Detect Hidden Bias in Company Policies Using AI
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Automatically identify, explain, and correct biased language in workplace policies. 
              Build a more inclusive organization with data-driven insights.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link to="/analyze">
                <Button size="lg" className="gap-2">
                  Analyze Policy
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link to="/demo">
                <Button variant="outline" size="lg">
                  View Demo
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="py-12 border-y border-border bg-muted/20">
        <div className="container">
          <div className="flex flex-wrap items-center justify-center gap-8 md:gap-16 text-muted-foreground">
            <div className="flex items-center gap-2">
              <Building2 className="h-5 w-5" />
              <span className="text-sm font-medium">Enterprise Ready</span>
            </div>
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              <span className="text-sm font-medium">SOC 2 Compliant</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              <span className="text-sm font-medium">500+ HR Teams</span>
            </div>
            <div className="flex items-center gap-2">
              <Scale className="h-5 w-5" />
              <span className="text-sm font-medium">Legal Approved</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 md:py-28">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Comprehensive Bias Detection
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Our AI analyzes your policies across multiple dimensions to ensure 
              fair and inclusive language throughout your organization.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<Search className="h-6 w-6" />}
              title="Deep Analysis"
              description="Scan policies for gender, age, disability, racial, and other forms of bias with advanced NLP."
            />
            <FeatureCard 
              icon={<AlertTriangle className="h-6 w-6" />}
              title="Clear Explanations"
              description="Understand why specific language is problematic with plain-English explanations."
            />
            <FeatureCard 
              icon={<Lightbulb className="h-6 w-6" />}
              title="Suggested Rewrites"
              description="Get inclusive alternatives for every biased phrase, ready to copy and implement."
            />
            <FeatureCard 
              icon={<BarChart3 className="h-6 w-6" />}
              title="Severity Scoring"
              description="Prioritize fixes with clear severity ratings from low to high impact."
            />
            <FeatureCard 
              icon={<FileText className="h-6 w-6" />}
              title="PDF Reports"
              description="Export detailed analysis reports for compliance records and stakeholder review."
            />
            <FeatureCard 
              icon={<CheckCircle className="h-6 w-6" />}
              title="History Tracking"
              description="Save and compare analyses over time to track your organization's progress."
            />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 md:py-28 bg-muted/30">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              How It Works
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Three simple steps to more inclusive policies.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <StepCard 
              step={1}
              title="Upload Policy"
              description="Paste your policy text or upload a document (PDF, DOCX, TXT)."
            />
            <StepCard 
              step={2}
              title="AI Analysis"
              description="Our AI scans for biased language across multiple categories."
            />
            <StepCard 
              step={3}
              title="Review & Fix"
              description="Review flagged items, understand issues, and apply suggested rewrites."
            />
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 md:py-28">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-6">
              Built for HR & Compliance Teams
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              PolicyGuard AI was designed specifically for enterprise HR teams, legal departments, 
              and policy writers who need a reliable, efficient way to ensure their workplace 
              policies promote inclusion and comply with anti-discrimination standards.
            </p>
            <p className="text-lg text-muted-foreground">
              Our AI model is trained on employment law, DEI best practices, and real-world 
              policy examples to provide accurate, actionable insights that help you build 
              a more equitable workplace.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 md:py-28 bg-primary text-primary-foreground">
        <div className="container text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to eliminate bias from your policies?
          </h2>
          <p className="text-lg opacity-90 mb-8 max-w-2xl mx-auto">
            Start analyzing your company policies today and create a more inclusive workplace.
          </p>
          <Link to="/analyze">
            <Button size="lg" variant="secondary" className="gap-2">
              Get Started Free
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>
    </Layout>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="p-6 rounded-lg border border-border bg-card hover:shadow-md transition-shadow">
      <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-card-foreground mb-2">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}

function StepCard({ step, title, description }: { step: number; title: string; description: string }) {
  return (
    <div className="text-center">
      <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-lg font-bold mx-auto mb-4">
        {step}
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}
