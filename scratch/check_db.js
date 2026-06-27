const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  'https://lifxtyhvgnxjjqgbzare.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI'
);

async function check() {
  const { data, error } = await supabase
    .from('tickets_taller')
    .select('folio, cliente, created_at');

  if (error) {
    console.error("Supabase error:", error);
    return;
  }

  console.log("Total Count:", data?.length);
  data?.forEach(t => {
    console.log(`Folio: ${t.folio} | Cliente: ${t.cliente} | Created At: ${t.created_at}`);
  });
}

check();
