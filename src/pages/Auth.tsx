import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Layout } from '@/components/layout';
import { useAuth } from '@/hooks/useAuth';
import { Shield, Mail, Lock, User, ArrowRight } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

export default function Auth() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user, login, signup } = useAuth();
  const { toast } = useToast();

  const [mode, setMode] = useState<'login' | 'signup'>(
    searchParams.get('mode') === 'signup' ? 'signup' : 'login'
  );
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (user) {
      navigate('/analyze');
    }
  }, [user, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    if (mode === 'login') {
      const result = login(email, password);
      if (result.success) {
        toast({ title: 'Welcome back!', description: 'You have been signed in successfully.' });
        navigate('/analyze');
      } else {
        toast({ title: 'Sign in failed', description: result.error, variant: 'destructive' });
      }
    } else {
      if (!name.trim()) {
        toast({ title: 'Name required', description: 'Please enter your name.', variant: 'destructive' });
        setIsLoading(false);
        return;
      }
      const result = signup(email, password, name);
      if (result.success) {
        toast({ title: 'Account created!', description: 'Welcome to PolicyGuard AI.' });
        navigate('/analyze');
      } else {
        toast({ title: 'Sign up failed', description: result.error, variant: 'destructive' });
      }
    }

    setIsLoading(false);
  };

  return (
    <Layout hideFooter>
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
              <Shield className="h-8 w-8 text-primary" />
            </div>
            <h1 className="text-2xl font-bold text-foreground">
              {mode === 'login' ? 'Welcome back' : 'Create your account'}
            </h1>
            <p className="text-muted-foreground mt-2">
              {mode === 'login' 
                ? 'Sign in to access your policy analyses' 
                : 'Get started with PolicyGuard AI'}
            </p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6 shadow-sm">
            <form onSubmit={handleSubmit} className="space-y-4">
              {mode === 'signup' && (
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="name"
                      type="text"
                      placeholder="John Smith"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="pl-10"
                      required={mode === 'signup'}
                    />
                  </div>
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10"
                    required
                    minLength={6}
                  />
                </div>
              </div>

              <Button type="submit" className="w-full gap-2" disabled={isLoading}>
                {isLoading ? 'Please wait...' : mode === 'login' ? 'Sign In' : 'Create Account'}
                <ArrowRight className="h-4 w-4" />
              </Button>
            </form>

            <div className="mt-6 text-center text-sm">
              {mode === 'login' ? (
                <p className="text-muted-foreground">
                  Don't have an account?{' '}
                  <button
                    type="button"
                    onClick={() => setMode('signup')}
                    className="text-primary hover:underline font-medium"
                  >
                    Sign up
                  </button>
                </p>
              ) : (
                <p className="text-muted-foreground">
                  Already have an account?{' '}
                  <button
                    type="button"
                    onClick={() => setMode('login')}
                    className="text-primary hover:underline font-medium"
                  >
                    Sign in
                  </button>
                </p>
              )}
            </div>
          </div>

          <p className="text-center text-xs text-muted-foreground mt-6">
            By continuing, you agree to our Terms of Service and Privacy Policy.
          </p>
        </div>
      </div>
    </Layout>
  );
}
