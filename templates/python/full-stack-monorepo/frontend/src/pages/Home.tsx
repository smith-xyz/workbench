import React, { useState, useEffect } from 'react';
import { apiClient, Card, Button, Loading } from '../common';

interface SystemStatus {
  engine: {
    status: string;
    config: unknown;
    version: string;
  };
  processor: {
    processor_type: string;
    config: unknown;
    status: string;
  };
}

const Home: React.FC = () => {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/core/status');
      setStatus(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch system status');
      console.error('Error fetching status:', err);
    } finally {
      setLoading(false);
    }
  };

  const testProcess = async () => {
    try {
      const testData = {
        id: 'test-frontend',
        data: { message: 'Hello from frontend!' }
      };

      const response = await apiClient.post('/core/process', testData);
      alert(`Processing result: ${response.data.status}`);
    } catch (err) {
      alert('Processing failed');
      console.error('Processing error:', err);
    }
  };

  if (loading) {
    return (
      <Card>
        <Loading text="Loading..." size="lg" />
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 dark:bg-red-900 mb-4">
            <svg className="h-6 w-6 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h1 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error</h1>
          <p className="text-gray-600 dark:text-gray-300 mb-4">{error}</p>
          <Button onClick={fetchStatus}>
            Retry
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Python Full-Stack Template</h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
            Welcome to the Python full-stack application template featuring:
          </p>
          <div className="max-w-md mx-auto">
            <ul className="text-left space-y-2 text-gray-700 dark:text-gray-300">
              <li className="flex items-center">
                <svg className="h-5 w-5 text-green-500 dark:text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                FastAPI backend with async support
              </li>
              <li className="flex items-center">
                <svg className="h-5 w-5 text-green-500 dark:text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                React frontend with TypeScript
              </li>
              <li className="flex items-center">
                <svg className="h-5 w-5 text-green-500 dark:text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                SQLAlchemy 2.0 with Alembic migrations
              </li>
              <li className="flex items-center">
                <svg className="h-5 w-5 text-green-500 dark:text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Comprehensive testing and development tools
              </li>
            </ul>
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">System Status</h2>
        {status && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3">Engine Status</h3>
              <div className="flex items-center space-x-4">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  status.engine.status === 'running' 
                    ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200' 
                    : 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                }`}>
                  <div className={`w-2 h-2 rounded-full mr-2 ${
                    status.engine.status === 'running' ? 'bg-green-400' : 'bg-red-400'
                  }`}></div>
                  {status.engine.status}
                </span>
                <span className="text-gray-600 dark:text-gray-300">
                  Version: <span className="font-medium">{status.engine.version}</span>
                </span>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3">Processor Status</h3>
              <div className="flex items-center space-x-4">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  status.processor.status === 'ready' 
                    ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200' 
                    : 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                }`}>
                  <div className={`w-2 h-2 rounded-full mr-2 ${
                    status.processor.status === 'ready' ? 'bg-green-400' : 'bg-red-400'
                  }`}></div>
                  {status.processor.status}
                </span>
                <span className="text-gray-600 dark:text-gray-300">
                  Type: <span className="font-medium">{status.processor.processor_type}</span>
                </span>
              </div>
            </div>
          </div>
        )}

        <div className="mt-6 flex space-x-4">
          <Button onClick={fetchStatus}>
            Refresh Status
          </Button>
          <Button variant="secondary" onClick={testProcess}>
            Test Processing
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default Home;
