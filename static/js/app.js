/* ==========================================================================
   TalentoRH · JavaScript del sitio
   - Mensajes y confirmaciones con SweetAlert2
   - Validación de formularios en el navegador (incluye RUT chileno)
   - Menú lateral en móviles, filtros automáticos y gráficos del dashboard
   ========================================================================== */

const COLOR_PRIMARIO = "#0f766e";

/* ---------- Mensajes de Flask con SweetAlert2 ---------- */
function mostrarMensajesFlash() {
  const nodo = document.getElementById("mensajes-flash");
  if (!nodo || !window.Swal) return;

  const mensajes = JSON.parse(nodo.textContent || "[]");
  mensajes.forEach(([categoria, texto]) => {
    const icono = ["success", "error", "warning", "info"].includes(categoria) ? categoria : "info";
    if (icono === "success" || icono === "info") {
      // Los mensajes positivos se muestran como aviso pequeño que se cierra solo
      Swal.fire({
        toast: true, position: "top-end", icon: icono, title: texto,
        showConfirmButton: false, timer: 3200, timerProgressBar: true,
      });
    } else {
      Swal.fire({
        icon: icono, title: icono === "error" ? "Atención" : "Aviso", text: texto,
        confirmButtonColor: COLOR_PRIMARIO, confirmButtonText: "Entendido",
      });
    }
  });
}

/* ---------- Confirmación antes de eliminar ---------- */
function activarConfirmaciones() {
  document.querySelectorAll("form[data-confirmar]").forEach((formulario) => {
    formulario.addEventListener("submit", async (evento) => {
      if (formulario.dataset.confirmado) return;
      evento.preventDefault();
      const respuesta = await Swal.fire({
        icon: "warning",
        title: "¿Estás seguro?",
        text: formulario.dataset.confirmar,
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#dc2626",
        reverseButtons: true,
        focusCancel: true,
      });
      if (respuesta.isConfirmed) {
        formulario.dataset.confirmado = "1";
        formulario.submit();
      }
    });
  });
}

/* ---------- RUT chileno ---------- */
const Rut = {
  limpiar: (rut) => rut.replace(/[^0-9kK]/g, "").toUpperCase(),

  calcularDv(cuerpo) {
    let suma = 0;
    let multiplicador = 2;
    for (let i = cuerpo.length - 1; i >= 0; i--) {
      suma += Number(cuerpo[i]) * multiplicador;
      multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }
    const resto = 11 - (suma % 11);
    return resto === 11 ? "0" : resto === 10 ? "K" : String(resto);
  },

  esValido(rut) {
    const limpio = Rut.limpiar(rut);
    if (limpio.length < 8) return false;
    const cuerpo = limpio.slice(0, -1);
    return /^\d+$/.test(cuerpo) && Rut.calcularDv(cuerpo) === limpio.slice(-1);
  },

  formatear(rut) {
    const limpio = Rut.limpiar(rut);
    if (limpio.length < 2) return limpio;
    const cuerpo = limpio.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return `${cuerpo}-${limpio.slice(-1)}`;
  },
};

function activarCamposRut() {
  document.querySelectorAll("input[data-rut]").forEach((input) => {
    input.addEventListener("input", () => {
      input.value = Rut.formatear(input.value);
      input.setCustomValidity("");
    });
    input.addEventListener("blur", () => {
      const valido = input.value === "" || Rut.esValido(input.value);
      input.setCustomValidity(valido ? "" : "El RUT no es válido (revisa el dígito verificador).");
      marcarCampo(input);
    });
  });
}

/* ---------- Validación de formularios ---------- */
function mensajeCampo(input) {
  if (input.validity.customError) return input.validationMessage;
  if (input.validity.valueMissing) return "Este campo es obligatorio.";
  if (input.validity.typeMismatch && input.type === "email") return "Ingresa un correo válido.";
  if (input.validity.tooShort) return `Debe tener al menos ${input.minLength} caracteres.`;
  if (input.validity.rangeUnderflow) return `El valor mínimo es ${input.min}.`;
  if (input.validity.rangeOverflow) return input.type === "date" ? "La fecha no puede ser futura." : `El valor máximo es ${input.max}.`;
  if (input.validity.patternMismatch) return "El formato no es válido.";
  return input.validationMessage;
}

function marcarCampo(input) {
  const campo = input.closest(".campo");
  if (!campo) return;
  const valido = input.checkValidity();
  campo.classList.toggle("invalido", !valido);

  let error = campo.querySelector(".error-campo");
  if (!valido) {
    if (!error) {
      error = document.createElement("span");
      error.className = "error-campo";
      campo.appendChild(error);
    }
    error.innerHTML = `<i class="bi bi-exclamation-circle"></i> ${mensajeCampo(input)}`;
  } else if (error) {
    error.remove();
  }
}

function activarValidacion() {
  document.querySelectorAll("form[data-validar]").forEach((formulario) => {
    const campos = formulario.querySelectorAll("input, select, textarea");

    campos.forEach((input) => {
      input.addEventListener("change", () => marcarCampo(input));
    });

    formulario.addEventListener("submit", (evento) => {
      campos.forEach(marcarCampo);
      if (!formulario.checkValidity()) {
        evento.preventDefault();
        const primero = formulario.querySelector(".campo.invalido input, .campo.invalido select, .campo.invalido textarea, :invalid");
        if (primero) primero.focus();
        Swal.fire({
          icon: "error",
          title: "Formulario incompleto",
          text: "Revisa los campos marcados en rojo antes de continuar.",
          confirmButtonColor: COLOR_PRIMARIO,
          confirmButtonText: "Entendido",
        });
      }
    });
  });
}

/* ---------- Sugerir sueldo según el cargo elegido ---------- */
function activarSugerenciaSueldo() {
  document.querySelectorAll("select[data-sugerir-sueldo]").forEach((select) => {
    const inputSueldo = document.getElementById(select.dataset.sugerirSueldo);
    if (!inputSueldo) return;
    select.addEventListener("change", () => {
      const sueldoBase = select.selectedOptions[0]?.dataset.sueldo;
      if (sueldoBase && !inputSueldo.value) {
        inputSueldo.value = sueldoBase;
        marcarCampo(inputSueldo);
      }
    });
  });
}

/* ---------- Otros detalles de la interfaz ---------- */
function activarVerPassword() {
  document.querySelectorAll("[data-ver-password]").forEach((boton) => {
    const input = document.getElementById(boton.dataset.verPassword);
    boton.addEventListener("click", () => {
      const oculto = input.type === "password";
      input.type = oculto ? "text" : "password";
      boton.innerHTML = `<i class="bi ${oculto ? "bi-eye-slash" : "bi-eye"}"></i>`;
    });
  });
}

function activarMenuMovil() {
  document.querySelectorAll("[data-abrir-menu]").forEach((boton) =>
    boton.addEventListener("click", () => document.body.classList.add("menu-abierto"))
  );
  document.querySelectorAll("[data-cerrar-menu]").forEach((fondo) =>
    fondo.addEventListener("click", () => document.body.classList.remove("menu-abierto"))
  );
}

function activarFiltrosAutomaticos() {
  document.querySelectorAll("form[data-filtros] [data-autoenviar]").forEach((select) =>
    select.addEventListener("change", () => select.form.submit())
  );
}

/* ---------- Gráficos del dashboard (Chart.js) ---------- */
function dibujarGraficos() {
  const nodo = document.getElementById("datos-graficos");
  if (!nodo || !window.Chart) return;
  const datos = JSON.parse(nodo.textContent);

  Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
  Chart.defaults.color = "#64748b";

  new Chart(document.getElementById("grafico-departamentos"), {
    type: "bar",
    data: {
      labels: datos.departamentos.etiquetas,
      datasets: [{
        label: "Trabajadores",
        data: datos.departamentos.valores,
        backgroundColor: COLOR_PRIMARIO,
        borderRadius: 8,
        maxBarThickness: 42,
      }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: "#eef2f6" } },
        x: { grid: { display: false } },
      },
    },
  });

  new Chart(document.getElementById("grafico-estados"), {
    type: "doughnut",
    data: {
      labels: datos.estados.etiquetas,
      datasets: [{
        data: datos.estados.valores,
        backgroundColor: ["#15803d", "#1d4ed8", "#d97706", "#94a3b8"],
        borderWidth: 3,
        borderColor: "#fff",
      }],
    },
    options: {
      maintainAspectRatio: false,
      cutout: "68%",
      plugins: { legend: { position: "bottom", labels: { usePointStyle: true, padding: 16 } } },
    },
  });
}

document.addEventListener("DOMContentLoaded", () => {
  mostrarMensajesFlash();
  activarConfirmaciones();
  activarCamposRut();
  activarValidacion();
  activarSugerenciaSueldo();
  activarVerPassword();
  activarMenuMovil();
  activarFiltrosAutomaticos();
  dibujarGraficos();
});
