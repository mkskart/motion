import React from 'react'

const LoginButton: React.FC = () => (
  <div className="flex items-center justify-center h-screen">
    <a
      href="http://localhost:8000/login"
      className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow"
    >
      Sign in with Google
    </a>
  </div>
)

export default LoginButton
