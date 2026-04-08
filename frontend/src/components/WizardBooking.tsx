import React, { useState, useEffect } from 'react';

/**
 * Basic Shell for Gratia Nail Art Booking Wizard
 * Translated from lapopnailslanding WizardBooking.js
 * 
 * TODO: Hook up to the FastAPI backend API_BASE_URL.
 * TODO: Obtain accurate service details and durations from client.
 * TODO: Set up dynamic prices and the exact flow.
 */

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

type FormData = {
  name: string;
  phone: string;
  email: string;
  serviceType: string;
  appointmentDate: string;
  appointmentTime: string;
};

export default function WizardBooking() {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [formData, setFormData] = useState<FormData>({
    name: '',
    phone: '',
    email: '',
    serviceType: '',
    appointmentDate: '',
    appointmentTime: '',
  });

  const nextStep = () => setCurrentStep((prev) => Math.min(prev + 1, 6));
  const prevStep = () => setCurrentStep((prev) => Math.max(prev - 1, 1));

  return (
    <div className="w-full max-w-4xl mx-auto min-h-[600px] flex flex-col bg-warm-beige rounded-3xl shadow-xl overflow-hidden border border-gold/20">
      {/* Header section */}
      <div className="bg-dark-deepest p-6 text-center shadow-md z-10 relative">
        <h2 className="font-headline text-3xl text-gold italic">Sistema de Reservas</h2>
        <p className="text-on-surface-variant font-body mt-2">
          Paso {currentStep} de 6 — {currentStep === 1 && "Datos personales"}
        </p>
      </div>

      {/* Body section */}
      <div className="p-8 flex-1 flex flex-col bg-light-cream">
        <div className="flex-1 flex items-center justify-center border-2 border-dashed border-dark-muted/30 rounded-2xl p-8 text-dark-muted">
          <p className="text-center font-body">
            Este es el esqueleto de la funcionalidad de reservas.<br />
            Estamos esperando la confirmación de los servicios y políticas de Hazael <br /> 
            para inyectar los precios, duración, fechas hábiles, etc.
          </p>
        </div>

        {/* Navigation placeholder */}
        <div className="mt-8 flex justify-between items-center w-full">
          <button 
            onClick={prevStep}
            disabled={currentStep === 1}
            className="px-6 py-2 rounded-full border border-gold text-dark-deepest font-label font-bold uppercase hover:bg-gold/10 transition-colors disabled:opacity-50"
          >
            Atrás
          </button>
          
          <button 
            onClick={nextStep}
            className="px-6 py-2 rounded-full bg-gold text-dark-deepest font-label font-bold uppercase shadow-md hover:brightness-110 transition-all hover:-translate-y-0.5"
          >
            Continuar
          </button>
        </div>
      </div>
    </div>
  );
}
