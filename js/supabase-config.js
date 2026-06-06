/**
 * Configuración Supabase (única fuente en frontend estático).
 * La anon key es pública por diseño; la seguridad real está en RLS + RPC.
 */
(function (global) {
  global.MacWaveSupabaseConfig = {
    url: 'https://lifxtyhvgnxjjqgbzare.supabase.co',
    anonKey:
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI',
  };
})(typeof window !== 'undefined' ? window : globalThis);
