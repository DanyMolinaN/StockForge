/*
 * POS frontend helper para integración futura.
 *
 * Este archivo es un punto de partida para el módulo web de Punto de Venta.
 * La lógica principal de la aplicación se ejecuta en el backend Python.
 */

window.StockForgePOS = {
    initialize: function () {
        console.log("POS module web starter loaded.");
    }
};

window.addEventListener("DOMContentLoaded", function () {
    StockForgePOS.initialize();
});
