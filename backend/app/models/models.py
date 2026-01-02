from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import bcrypt
import uuid

Base = declarative_base()


class User(Base):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    analyses = relationship("AnalysisResult", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class AnalysisResult(Base):
    """Analysis result model"""
    __tablename__ = 'analysis_results'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), index=True)
    policy_name = Column(String(255), nullable=False)
    policy_text = Column(Text, nullable=False)
    total_bias_count = Column(Integer, default=0)
    overall_severity = Column(String(20), default='low')  # low, medium, high
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    bias_instances = relationship("BiasInstance", back_populates="analysis", cascade="all, delete-orphan")
    
    def to_dict(self, include_text=True):
        """Convert to dictionary"""
        result = {
            'id': self.id,
            'policyName': self.policy_name,
            'analyzedAt': self.analyzed_at.isoformat() if self.analyzed_at else None,
            'totalBiasCount': self.total_bias_count,
            'overallSeverity': self.overall_severity,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_text:
            result['policyText'] = self.policy_text
            
        if self.bias_instances:
            result['biasInstances'] = [b.to_dict() for b in self.bias_instances]
            
        return result


class BiasInstance(Base):
    """Bias instance model"""
    __tablename__ = 'bias_instances'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String(36), ForeignKey('analysis_results.id', ondelete='CASCADE'), index=True)
    original_text = Column(String(500), nullable=False)
    bias_type = Column(String(50), nullable=False)  # gender, age, disability, racial, other
    severity = Column(String(20), nullable=False)  # low, medium, high
    explanation = Column(Text, nullable=False)
    suggested_rewrite = Column(String(500), nullable=False)
    start_index = Column(Integer, nullable=False)
    end_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    analysis = relationship("AnalysisResult", back_populates="bias_instances")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'originalText': self.original_text,
            'biasType': self.bias_type,
            'severity': self.severity,
            'explanation': self.explanation,
            'suggestedRewrite': self.suggested_rewrite,
            'startIndex': self.start_index,
            'endIndex': self.end_index,
        }
