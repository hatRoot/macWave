const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  'https://lifxtyhvgnxjjqgbzare.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI'
);

async function check() {
  const { data, error } = await supabase
    .from('ordenes_servicio')
    .select('*')
    .order('updated_at', { ascending: false })
    .limit(3);

  if (error) {
    console.error("Supabase error:", error);
    return;
  }

  data.forEach(ods => {
    console.log("=========================================");
    console.log(`Folio: ${ods.folio}`);
    console.log(`ID: ${ods.id}`);
    console.log(`Cliente: ${ods.cliente}`);
    console.log(`Status: ${ods.status}`);
    console.log(`Updated At: ${ods.updated_at}`);
    
    // Inspect notes/historial
    try {
      const hist = JSON.parse(ods.notas || '[]');
      console.log(`Notas JSON length: ${hist.length}`);
      hist.forEach((entry, idx) => {
        console.log(`  Entry ${idx + 1}:`);
        console.log(`    Date: ${entry.date}`);
        console.log(`    Status: ${entry.status}`);
        console.log(`    Text: ${entry.text}`);
        if (entry.img) {
          console.log(`    Legacy img present: ${entry.img.substring(0, 50)}...`);
        }
        if (entry.photos) {
          console.log(`    Photos array length: ${entry.photos.length}`);
          entry.photos.forEach((ph, pIdx) => {
            console.log(`      Photo ${pIdx + 1}: ${ph ? ph.substring(0, 60) : 'null'} (length: ${ph ? ph.length : 0})`);
          });
        }
      });
    } catch (e) {
      console.log(`Notas raw: ${ods.notas ? ods.notas.substring(0, 100) : 'null'}...`);
    }
  });
}

check();
