// =====================================================
// CONFIGURACIÓN MQTT Y LÓGICA PRINCIPAL
// =====================================================

const FLESPI_TOKEN = "QwWWJaPQ5ptFVTdPpQ3b17e8jIPY7Kv9H7bfCRKiFcNW1ZAqaeC3u0SQhgMODpYs";
const MQTT_SERVER = "wss://mqtt.flespi.io";

const options = {
    username: FLESPI_TOKEN,
    password: "", 
    clientId: "mi_dashboard_web_" + Math.random().toString(16).substr(2, 8),
};

console.log("Conectando a Flespi...");
const client = mqtt.connect(MQTT_SERVER, options);
const statusElement = document.getElementById('status-conexion');

// Iniciamos el mapa cuando la página cargue
window.addEventListener('load', iniciarMapa);

client.on("connect", () => {
    console.log("¡Conectado exitosamente a Flespi!");
    if(statusElement) {
        statusElement.innerText = "Conectado";
        statusElement.style.color = "#28a745"; 
    }
    // Nos suscribimos a todo
    client.subscribe("iotzi/escuela/sensor/#");
});

client.on("message", (topic, message) => {
    try {
        const msg = message.toString();
        const data = JSON.parse(msg); 

        // 1. Humo
        if (topic.includes("humo")) {
            actualizarTarjeta('humo', data.smoke_value, data.status);
        } 
        // 2. Gas
        else if (topic.includes("gas")) {
            actualizarTarjeta('gas', data.gas_value, data.status);
        }
        // 3. PM2.5
        else if (topic.includes("pm25")) {
            actualizarTarjeta("pm25", data.pm_valor, data.status);
        }
        // 4. Ruido
        else if (topic.includes("ruido")) {
            actualizarTarjeta('ruido', data.noise_db, data.noise_level);
        }
        // 5. CO (Evitamos conflicto con IndiceC)
        else if (topic.includes("co") && !topic.includes("IndiceC")) {
            actualizarTarjeta('co', data.co_ppm, data.co_status);
        }
        // 6. Viento
        else if (topic.includes("vien")) {
            const valEl = document.getElementById('viento-valor');
            const dirEl = document.getElementById('viento-dir');
            if(valEl && data.wind_speed_kmh) valEl.innerText = data.wind_speed_kmh.toFixed(1);
            if(dirEl && data.wind_direction_cardinal) dirEl.innerText = data.wind_direction_cardinal;
        }
        // 7. Temperatura
        else if (topic.includes("temp")) {
            const temp = data.val; 
            let estadoTemp = "NORMAL";
            if (temp >= 35) estadoTemp = "DANGER"; 
            else if (temp >= 30) estadoTemp = "WARNING";
            else if (temp <= 10) estadoTemp = "WARNING";
            actualizarTarjeta('temp', temp.toFixed(1), estadoTemp);
        }
        // 8. Humedad
        else if (topic.includes("hum") && !topic.includes("humo")) { 
            const hum = data.val;
            let estadoHumedad = "NORMAL";
            if (hum > 70) estadoHumedad = "WARNING"; 
            else if (hum < 30) estadoHumedad = "WARNING"; 
            actualizarTarjeta('humedad', hum.toFixed(1), estadoHumedad);
        }
        // 9. Oxígeno (DO)
        else if (topic.includes("do")) {
            // Leemos los datos correctos de tu simulación
            const oxigeno = data.oxygen_mg_L; 
            const estadoDo = data.status; 
            actualizarTarjeta('do', oxigeno, estadoDo);
        }
        // 10. Índice de Calor
        else if (topic.includes("IndiceC")) {
            const tempReal = data.temperature_c;
            const sensacion = data.heat_index_c;
            
            const tRealEl = document.getElementById('indicec-temp');
            const valEl = document.getElementById('indicec-valor');
            const estEl = document.getElementById('indicec-estado');
            
            if(tRealEl) tRealEl.innerText = tempReal.toFixed(1);
            if(valEl) valEl.innerText = sensacion.toFixed(1);
            
            let estado = "NORMAL";
            if (sensacion >= 54) estado = "DANGER";
            else if (sensacion >= 41) estado = "DANGER";
            else if (sensacion >= 32) estado = "WARNING";
            
            if(estEl) estEl.innerText = estado;
            actualizarClasesCSS('indicec', estado);
            
            if(typeof actualizarMarcadorMapa === 'function') {
                actualizarMarcadorMapa('indicec', estado);
            }
        }

    } catch (e) {
        console.error("Error:", e);
    }
});

client.on("error", (err) => {
    console.error("Error conexión:", err);
});

function actualizarTarjeta(prefijo, valor, estado) {
    const valorEl = document.getElementById(`${prefijo}-valor`);
    const estadoEl = document.getElementById(`${prefijo}-estado`);
    
    if (valorEl && valor !== undefined) valorEl.innerText = valor;
    if (estadoEl && estado !== undefined) estadoEl.innerText = estado;

    actualizarClasesCSS(prefijo, estado);

    if(typeof actualizarMarcadorMapa === 'function') {
        actualizarMarcadorMapa(prefijo, estado);
    }
}

function actualizarClasesCSS(prefijo, estado) {
    const cardEl = document.getElementById(`card-${prefijo}`);
    if (!cardEl) return;

    const dangerStates = ["DANGER", "POOR", "VERY_LOUD", "HIGHLY_DANGEROUS", "CRITICAL", "LOW"];
    const warningStates = ["ELEVATED", "MODERATE", "WARNING", "SUPERSATURATION", "HIGH"]; 
    
    if (dangerStates.includes(estado)) {
        cardEl.classList.add("danger");
        cardEl.classList.remove("warning");
        cardEl.classList.remove("normal");
    } else if (warningStates.includes(estado)) {
        cardEl.classList.remove("danger");
        cardEl.classList.add("warning");
        cardEl.classList.remove("normal");
    } else {
        cardEl.classList.remove("danger");
        cardEl.classList.remove("warning");
        cardEl.classList.add("normal");
    }
}

// =====================================================
// LÓGICA DEL MAPA (LEAFLET)
// =====================================================

let map;
let sensoresMap = {};
let iconGreen, iconOrange, iconRed;

function iniciarMapa() {
    // Buscamos el div del mapa que YA existe en el HTML
    const mapDiv = document.getElementById('map');
    if(!mapDiv) return; 
    if(map) return; // Evitar doble inicio

    console.log("Iniciando Mapa ITT...");

    const centroCampus = [32.529922, -116.987100];
    
    map = L.map('map').setView(centroCampus, 18); 

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Iconos
    const LeafIcon = L.Icon.extend({
        options: {
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
            shadowSize: [41, 41]
        }
    });

    iconGreen = new LeafIcon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png' });
    iconOrange = new LeafIcon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png' });
    iconRed = new LeafIcon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png' });

    // Pines en el mapa
    sensoresMap = {
        'pm25':    L.marker([32.529922, -116.987100], {icon: iconGreen}).addTo(map).bindPopup("<b>PM2.5</b><br>Plaza Cívica"),
        'ruido':   L.marker([32.529400, -116.988500], {icon: iconGreen}).addTo(map).bindPopup("<b>Ruido</b><br>Entrada Galgo"),
        'viento':  L.marker([32.530800, -116.987800], {icon: iconGreen}).addTo(map).bindPopup("<b>Viento</b><br>Teatro Cala-Fornix"),
        'temp':    L.marker([32.530500, -116.986800], {icon: iconGreen}).addTo(map).bindPopup("<b>Temperatura</b><br>Biblioteca"),
        'humo':    L.marker([32.530200, -116.987200], {icon: iconGreen}).addTo(map).bindPopup("<b>Humo</b><br>Cafetería"),
        'gas':     L.marker([32.530600, -116.985500], {icon: iconGreen}).addTo(map).bindPopup("<b>Gas</b><br>Laboratorios Química"),
        'do':      L.marker([32.530400, -116.986200], {icon: iconGreen}).addTo(map).bindPopup("<b>Oxígeno</b><br>Edificio Académico"),
        'co':      L.marker([32.531500, -116.987000], {icon: iconGreen}).addTo(map).bindPopup("<b>CO</b><br>Estacionamiento Norte"),
        'indicec': L.marker([32.529000, -116.986000], {icon: iconGreen}).addTo(map).bindPopup("<b>Índice Calor</b><br>Campo Deportivo"),
        'humedad': L.marker([32.528800, -116.987500], {icon: iconGreen}).addTo(map).bindPopup("<b>Humedad</b><br>Jardines Sur")
    };
}

function actualizarMarcadorMapa(prefijo, estado) {
    if (!map || !sensoresMap[prefijo]) return;

    const marcador = sensoresMap[prefijo];
    const dangerStates = ["DANGER", "POOR", "VERY_LOUD", "HIGHLY_DANGEROUS", "CRITICAL", "LOW"];
    const warningStates = ["ELEVATED", "MODERATE", "WARNING", "SUPERSATURATION", "HIGH"];

    if (dangerStates.includes(estado)) {
        marcador.setIcon(iconRed);
        marcador.openPopup(); 
    } else if (warningStates.includes(estado)) {
        marcador.setIcon(iconOrange);
    } else {
        marcador.setIcon(iconGreen);
        marcador.closePopup();
    }
}