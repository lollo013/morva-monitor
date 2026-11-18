/* Un errore della voce ha sempre un codice leggibile dalla dashboard. */
export class ErroreVoce extends Error {
  constructor(codice, messaggio, dettagli = {}) {
    super(messaggio);
    this.name = 'ErroreVoce';
    this.codice = codice;
    this.dettagli = dettagli;
  }
}
