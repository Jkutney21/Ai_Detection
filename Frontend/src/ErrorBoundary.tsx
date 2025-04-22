import React, { Component, ReactNode } from 'react';

// This component will catch errors in its children
class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean }> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): { hasError: boolean } {
    // Update state to indicate an error has occurred
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo): void {
    // Log the error to an error reporting service (optional)
    console.error('Error caught by ErrorBoundary:', error, info);
  }

  render() {
    if (this.state.hasError) {
      // You can customize the fallback UI
      return <h2>Something went wrong. Please try again later.</h2>;
    }

    return this.props.children; // Render the child components if no error
  }
}

export default ErrorBoundary;
