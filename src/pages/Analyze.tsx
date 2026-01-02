import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Layout } from '@/components/layout';
import { useAuth } from '@/hooks/useAuth';
import { generateMockAnalysis, samplePolicyText } from '@/lib/mockData';
import { analysisStorage } from '@/lib/auth';
import { FileText, Upload, ArrowRight, Loader2, Sparkles } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

export default function Analyze() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { toast } = useToast();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [policyName, setPolicyName] = useState('');
  const [policyText, setPolicyText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const allowedTypes = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (file.type === 'text/plain') {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        setPolicyText(text);
        setFileName(file.name);
        setSelectedFile(null); // Clear file if text is loaded
        if (!policyName) {
          setPolicyName(file.name.replace(/\.[^/.]+$/, ''));
        }
      };
      reader.readAsText(file);
    } else if (['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(file.type)) {
      // Store file in state for later upload
      setSelectedFile(file);
      setFileName(file.name);
      setPolicyText(''); // Clear text if file is uploaded
      if (!policyName) {
        setPolicyName(file.name.replace(/\.[^/.]+$/, ''));
      }
      toast({
        title: 'File selected',
        description: `"${file.name}" will be parsed when you analyze it.`,
      });
    } else {
      toast({
        title: 'Unsupported file type',
        description: 'Please upload a TXT, PDF, or DOCX file.',
        variant: 'destructive',
      });
    }
  };

  const handleAnalyze = async () => {
    // Check if we have either text or a file
    if (!policyText.trim() && !selectedFile) {
      toast({
        title: 'Policy text required',
        description: 'Please paste text or upload a policy to analyze.',
        variant: 'destructive',
      });
      return;
    }

    setIsAnalyzing(true);

    try {
      // Check if backend is available
      const backendURL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      
      let response;
      
      // If we have a selected file, send it to backend for parsing
      if (selectedFile) {
        console.log('Sending file to backend:', selectedFile.name);
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('policyName', policyName || selectedFile.name);
        
        response = await fetch(`${backendURL}/api/analysis/analyze`, {
          method: 'POST',
          ...(user && { headers: { 'Authorization': `Bearer ${user.token}` } }),
          body: formData,
        });
      } else {
        // Send as JSON with text
        console.log('Sending text to backend');
        response = await fetch(`${backendURL}/api/analysis/analyze`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(user && { 'Authorization': `Bearer ${user.token}` }),
          },
          body: JSON.stringify({
            policyText: policyText.trim(),
            policyName: policyName || 'Untitled Policy',
          }),
        });
      }

      if (!response.ok) {
        const error = await response.json();
        console.error('Backend error:', error);
        toast({
          title: 'Analysis failed',
          description: error.error || 'Failed to analyze policy',
          variant: 'destructive',
        });
        setIsAnalyzing(false);
        return;
      }

      const data = await response.json();
      console.log('Analysis response:', data);
      if (data.success) {
        // Clear file selection
        setSelectedFile(null);
        setIsAnalyzing(false);
        navigate(`/results/${data.data.id}`, { state: { analysis: data.data } });
      } else {
        toast({
          title: 'Analysis failed',
          description: 'Backend returned error',
          variant: 'destructive',
        });
        setIsAnalyzing(false);
      }
    } catch (error) {
      console.error('Analysis error:', error);
      // Fallback to mock analysis if backend is not available
      toast({
        title: 'Using demo mode',
        description: 'Backend not available. Using sample analysis.',
      });

      const analysis = generateMockAnalysis(
        policyText,
        policyName || 'Untitled Policy'
      );

      if (user) {
        analysisStorage.save(analysis);
      }

      setIsAnalyzing(false);
      navigate(`/results/${analysis.id}`, { state: { analysis } });
    }
  };

  const loadSamplePolicy = () => {
    setPolicyText(samplePolicyText);
    setPolicyName('Sample Employee Conduct Policy');
    toast({
      title: 'Sample loaded',
      description: 'A sample policy with various bias examples has been loaded.',
    });
  };

  return (
    <Layout>
      <div className="container py-12 md:py-20">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-10">
            <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Analyze Your Policy
            </h1>
            <p className="text-lg text-muted-foreground">
              Paste your policy text or upload a document to detect potential bias.
            </p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6 md:p-8 shadow-sm">
            <div className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="policyName">Policy Name (optional)</Label>
                <Input
                  id="policyName"
                  placeholder="e.g., Employee Conduct Policy"
                  value={policyName}
                  onChange={(e) => setPolicyName(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="policyText">Policy Text</Label>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={loadSamplePolicy}
                    className="text-primary gap-1"
                  >
                    <Sparkles className="h-3 w-3" />
                    Load sample
                  </Button>
                </div>
                <Textarea
                  id="policyText"
                  placeholder="Paste your company policy text here..."
                  value={policyText}
                  onChange={(e) => setPolicyText(e.target.value)}
                  className="min-h-[300px] font-mono text-sm"
                />
              </div>

              <div className="flex items-center gap-4">
                <div className="flex-1 h-px bg-border" />
                <span className="text-sm text-muted-foreground">or</span>
                <div className="flex-1 h-px bg-border" />
              </div>

              <div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.pdf,.docx"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                <Button
                  type="button"
                  variant="outline"
                  className="w-full gap-2"
                  onClick={() => fileInputRef.current?.click()}
                >
                  <Upload className="h-4 w-4" />
                  Upload Document (PDF, DOCX, TXT)
                </Button>
                {fileName && (
                  <p className="text-sm text-muted-foreground mt-2 flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    {fileName}
                  </p>
                )}
              </div>

              <Button
                onClick={handleAnalyze}
                disabled={isAnalyzing || !policyText.trim()}
                size="lg"
                className="w-full gap-2"
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    Analyze Policy
                    <ArrowRight className="h-4 w-4" />
                  </>
                )}
              </Button>

              {!user && (
                <p className="text-sm text-muted-foreground text-center">
                  <a href="/auth" className="text-primary hover:underline">Sign in</a> to save your analyses
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
