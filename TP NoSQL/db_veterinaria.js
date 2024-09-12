use TPNoSQL;

db.createCollection("pacientes");

db.pacientes.insertMany([
  {
    nombre: "Oliver",
    especie: "Perro",
    raza: "Caniche",
    edad: 1,
    dueño: {
      nombre: "Pablo Torrez",
      telefono: "123456789"
    }
  },
  {
    nombre: "Emma",
    especie: "Gato",
    raza: "Siames",
    edad: 2,
    dueño: {
      nombre: "Ana Gomez",
      telefono: "987654321"
    }
  }
]);

db.pacientes.find();

db.createCollection("veterinarios");

db.veterinarios.insertMany([
  {
    nombre: "Dr. Juan Rodríguez",
    especialidad: "Cirugia",
    telefono: "123456789"
  }
]);

db.veterinarios.find();

// Para ejecutar este script desde la consola:
// mongo <db_veterinaria.js>