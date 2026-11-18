/* =====================================================================
   Configurazione della voce ufficiale del Professor Aurelio.

   La voce si sceglie una volta sola, dalla dashboard privata. Finche' il
   file di configurazione non dice "approvata" con un voice_id, nessuna
   narrazione parte: non esiste una voce di riserva.
   ===================================================================== */
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { ErroreVoce } from './errori.mjs';

export const FILE_CONFIG = path.join(
  path.dirname(fileURLToPath(import.meta.url)), '..', 'config', 'voce.json'
);

export async function leggiConfig(file = FILE_CONFIG) {
  return JSON.parse(await readFile(file, 'utf8'));
}

/* Restituisce la configurazione solo se la voce e' stata approvata. */
export function voceApprovata(config) {
  if (config.stato !== 'approvata' || !config.voice_id) {
    throw new ErroreVoce(
      'VOCE_NON_APPROVATA',
      'La voce ufficiale del Professor Aurelio non e\' ancora stata approvata. ' +
      'Sceglila dalla dashboard privata prima di produrre qualsiasi video.'
    );
  }
  return config;
}
