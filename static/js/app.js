/* ==========================================================================
   TalentoRH · JavaScript
   1. Mensajes de Flask con SweetAlert2
   2. Confirmación antes de eliminar
   3. RUT chileno (formato y dígito verificador)
   4. Validación de formularios en el navegador
   5. Filtros que se aplican solos
   6. Gráfico del dashboard (Chart.js)
   ========================================================================== */

const COLOR_PRINCIPAL = "#0f766e";

/* 1. Mensajes de Flask con SweetAlert2 */
function mostrarMensajes() {
  const mensajes = JSON.parse(document.getElementById("mensajes").textContent);

  for (const [tipo, texto] of mensajes) {
    if (tipo === "success") {
      // Los mensajes de éxito aparecen en una esquina y se cierran solos
      Swal.fire({ toast: true, position: "top-end", icon: "success", title: texto,
                  showConfirmButton: false, timer: 3000, timerProgressBar: true });
    } else {
      Swal.fire({ icon: tipo === "error" ? "error" : "warning", title: "Atención", text: texto,
                  confirmButtonColor: COLOR_PRINCIPAL, confirmButtonText: "Entendido" });
    }
  }
}

/* 2. Confirmación antes de eliminar (formularios con data-confirmar) */
function activarConfirmaciones() {
  document.querySelectorAll("form[data-confirmar]").forEach((formulario) => {
    formulario.addEventListener("submit", async (evento) => {
      evento.preventDefault();
      const respuesta = await Swal.fire({
        icon: "warning",
        title: "¿Eliminar trabajador?",
        text: formulario.dataset.confirmar,
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#dc2626",
        reverseButtons: true,
      });
      if (respuesta.isConfirmed) {
        formulario.submit(); // submit() no vuelve a disparar este evento
      }
    });
  });
}

/* 3. RUT chileno */
function limpiarRut(rut) {
  return rut.replace(/[^0-9kK]/g, "").toUpperCase();
}

function calcularDv(numero) {
  let suma = 0;
  let multiplicador = 2;
  for (let i = numero.length - 1; i >= 0; i--) {
    suma += Number(numero[i]) * multiplicador;
    multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
  }
  const resto = 11 - (suma % 11);
  if (resto === 11) return "0";
  if (resto === 10) return "K";
  return String(resto);
}

function rutValido(rut) {
  const limpio = limpiarRut(rut);
  const numero = limpio.slice(0, -1);
  return limpio.length >= 8 && /^\d+$/.test(numero) && calcularDv(numero) === limpio.slice(-1);
}

function formatearRut(rut) {
  const limpio = limpiarRut(rut);
  if (limpio.length < 2) return limpio;
  const numero = limpio.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return `${numero}-${limpio.slice(-1)}`;
}

function activarCampoRut() {
  const input = document.querySelector("input[data-rut]");
  if (!input) return;

  // Mientras se escribe, se agregan los puntos y el guion
  input.addEventListener("input", () => {
    input.value = formatearRut(input.value);
    input.setCustomValidity("");
  });
  // Al salir del campo, se revisa el dígito verificador
  input.addEventListener("blur", () => {
    const valido = input.value === "" || rutValido(input.value);
    input.setCustomValidity(valido ? "" : "El RUT no es válido.");
    marcarCampo(input);
  });
}

/* 4. Validación de formularios (formularios con data-validar) */
function mensajeDeError(input) {
  if (input.validity.valueMissing) return "Este campo es obligatorio.";
  if (input.validity.customError) return input.validationMessage;
  if (input.validity.typeMismatch) return "El correo no tiene un formato válido.";
  if (input.validity.tooShort) return `Debe tener al menos ${input.minLength} caracteres.`;
  if (input.validity.rangeOverflow) return "La fecha de ingreso no puede ser futura.";
  if (input.validity.rangeUnderflow || input.validity.badInput) return "Ingresa un sueldo válido.";
  if (input.validity.patternMismatch) return "El teléfono no es válido.";
  return input.validationMessage;
}

function marcarCampo(input) {
  const campo = input.closest(".campo");
  const valido = input.checkValidity();
  campo.classList.toggle("invalido", !valido);

  let error = campo.querySelector(".error-campo");
  if (valido) {
    if (error) error.remove();
    return;
  }
  if (!error) {
    error = document.createElement("span");
    error.className = "error-campo";
    campo.appendChild(error);
  }
  error.textContent = mensajeDeError(input);
}

function activarValidacion() {
  document.querySelectorAll("form[data-validar]").forEach((formulario) => {
    const campos = formulario.querySelectorAll("input, select");
    campos.forEach((input) => input.addEventListener("change", () => marcarCampo(input)));

    formulario.addEventListener("submit", (evento) => {
      campos.forEach(marcarCampo);
      if (!formulario.checkValidity()) {
        evento.preventDefault();
        Swal.fire({ icon: "error", title: "Faltan datos",
                    text: "Revisa los campos marcados en rojo.",
                    confirmButtonColor: COLOR_PRINCIPAL, confirmButtonText: "Entendido" });
      }
    });
  });
}

/* 5. En el listado, los filtros se aplican apenas se elige una opción */
function activarFiltros() {
  document.querySelectorAll("select[data-enviar-al-cambiar]").forEach((select) => {
    select.addEventListener("change", () => select.form.submit());
  });
}

/* 6. Gráfico de barras del dashboard */
function dibujarGrafico() {
  const datos = document.getElementById("datos-grafico");
  if (!datos || !window.Chart) return;
  const porDepartamento = JSON.parse(datos.textContent);

  Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
  new Chart(document.getElementById("grafico-departamentos"), {
    type: "bar",
    data: {
      labels: Object.keys(porDepartamento),
      datasets: [{
        label: "Trabajadores",
        data: Object.values(porDepartamento),
        backgroundColor: COLOR_PRINCIPAL,
        borderRadius: 8,
        maxBarThickness: 48,
      }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 } },
        x: { grid: { display: false } },
      },
    },
  });
}

document.addEventListener("DOMContentLoaded", () => {
  mostrarMensajes();
  activarConfirmaciones();
  activarCampoRut();
  activarValidacion();
  activarFiltros();
  dibujarGrafico();
});
