'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import axios from 'axios'; // Still need this for the signin call since it doesn't require auth yet

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted'); // Step 1
    
    setError(null);
    setLoading(true);
    console.log('Loading set to true'); // Step 2
    
    try {
      console.log('Making API call...'); // Step 3
      const response = await axios.post('http://localhost:8000/auth/login', {
        email,
        password,
      });
      console.log('API response received:', response.data); // Step 4
      
      // Extract and store token
      const { access_token, user_id, email: userEmail } = response.data;
      
      // Store in localStorage
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_id', user_id.toString());
      localStorage.setItem('email', userEmail);
      
      // Verify token was stored
      const storedToken = localStorage.getItem('access_token');
      console.log('Token stored:', storedToken ? 'YES' : 'NO');
      console.log('Stored token value:', storedToken);
      
      console.log('Attempting redirect...'); // Step 6
      // Small delay to ensure token is properly stored
      await new Promise(resolve => setTimeout(resolve, 100));
      // Force redirect using window.location to ensure navigation
      window.location.href = '/dashboard';
      console.log('Redirect initiated'); // Step 7 - Should not appear if redirect works
      
    } catch (err: any) {
      console.error('Full error object:', err); // Always log errors
      console.error('Error response:', err.response);
      console.error('Error request:', err.request);
      
      // Handle different error types
      if (err.response) {
        // Server responded with error status
        setError(err.response.data?.detail || 'Authentication failed');
      } else if (err.request) {
        // Request was made but no response received
        setError('Network error. Please try again.');
      } else {
        // Something else happened
        setError('An unexpected error occurred');
      }
    } finally {
      // Always reset loading state
      setLoading(false);
      console.log('Loading set to false'); // Step 8
    }
  };

  return (
    <div className="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
          Sign in to your account
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Or{' '}
          <Link href="/signup" className="font-medium text-indigo-600 hover:text-indigo-500">
            create a new account
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {error && (
            <div className="mb-4 rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">{error}</h3>
                </div>
              </div>
            </div>
          )}

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div className="mt-1">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">
                  Forgot your password?
                </a>
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Signing in...' : 'Sign in'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}