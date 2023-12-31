import ReactDOM from 'react-dom/client'
import './index.css'
import { GoogleOAuthProvider } from '@react-oauth/google'
import router from './routes.tsx'
import { RouterProvider } from 'react-router-dom'
import { Elements } from '@stripe/react-stripe-js'
import { loadStripe } from '@stripe/stripe-js'

const stripeKey = import.meta.env.VITE_STRIPE_KEY || "your_publish_key"
const stripePromise = loadStripe(stripeKey);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Elements stripe={stripePromise}>
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID || "error"}>
      <RouterProvider router={router} />
    </GoogleOAuthProvider>
  </Elements>

)
