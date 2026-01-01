import { Shield } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-border bg-muted/30">
      <div className="container py-8 md:py-12">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Shield className="h-6 w-6 text-primary" />
            <span className="font-semibold text-foreground">PolicyGuard AI</span>
          </div>
          <p className="text-sm text-muted-foreground text-center md:text-left">
            AI-powered bias detection for fairer, more inclusive company policies.
          </p>
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} PolicyGuard AI
          </p>
        </div>
      </div>
    </footer>
  );
}
