import React from 'react';

export const Button = ({ 
  children, 
  variant = 'primary', 
  className = '', 
  href,
  onClick,
  ariaLabel,
  ...props 
}) => {
  const baseStyles = 'inline-flex items-center justify-center px-6 py-3 rounded-full font-medium transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-green-200 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-gradient-to-r from-green-500 to-green-600 text-white hover:from-green-600 hover:to-green-700 shadow-lg hover:shadow-xl hover:scale-105',
    outline: 'border-2 border-green-600 text-green-600 hover:bg-green-50 hover:border-green-700 hover:text-green-700',
  };

  const combinedClassName = `${baseStyles} ${variants[variant]} ${className}`;

  if (href) {
    return (
      <a 
        href={href}
        className={combinedClassName}
        aria-label={ariaLabel}
        {...props}
      >
        {children}
      </a>
    );
  }

  return (
    <button 
      className={combinedClassName}
      onClick={onClick}
      aria-label={ariaLabel}
      {...props}
    >
      {children}
    </button>
  );
};
