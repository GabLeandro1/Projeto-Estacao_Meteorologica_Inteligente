// SIDEBAR TOGGLE

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function OpenSidebar(){
    if(!sidebarOpen){
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true;
    }
}

function closeSidebar(){
    if(sidebarOpen) {
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen = false;
    }
}

// Função para converter data do formato "DD/MM/YYYY, HH:mm:ss" para Timestamp (ms)
function parseDataISO(dataStr) {
  // Exemplo de entrada: "01/09/2026, 00:05:30"
  const [dataPart, horaPart] = dataStr.split(', ');
  const [dia, mes, ano] = dataPart.split('/');
  
  // Retorna o timestamp em milissegundos
  return new Date(`${ano}-${mes}-${dia}T${horaPart}`).getTime();
}

// Carregar o arquivo CSV usando PapaParse
Papa.parse('dados_estacao_meteorologica_set_out_2026.csv', {
  download: true,
  header: true,
  delimiter: ';',
  skipEmptyLines: true,
  complete: function(results) {
    const rawData = results.data;
    
    // Arrays formatados para o ApexCharts no padrão [timestamp, valor]
    const serieTemperatura = [];
    const serieUmidade = [];
    const seriePressao = [];
    const serieChuva = [];
    const serieDispersao = [];
    const serieLuz = [];

    rawData.forEach(row => {
      if (!row['Data']) return;

      const timestamp = parseDataISO(row['Data']);
      
      // Sanitização e conversão de tipos
      const temp = parseFloat(row['Temperatura'].replace(' °C', '').trim());
      const umidade = parseFloat(row['Umidade'].replace(' %', '').trim());
      const pressao = parseFloat(row['Pressão'].replace(' hPa', '').trim());
      const chuva = parseInt(row['Chuva']);
      const luz = parseInt(row['Luminosidade']);

      // Adiciona no formato de coordenada [x, y]
      serieTemperatura.push([timestamp, temp]);
      serieUmidade.push([timestamp, umidade]);
      seriePressao.push([timestamp, pressao]);
      serieChuva.push([timestamp, chuva]);
      serieDispersao.push([temp, umidade]);
      serieLuz.push([timestamp, luz]);
    });

    // Renderizar os gráficos com os dados prontos
    renderizarGraficoTempUmidade(serieTemperatura, serieUmidade);
    renderizarGraficoPressao(seriePressao);
    renderizarGraficoDispersao(serieDispersao);
    renderizarGraficoEventos(serieLuz, serieChuva);
  }
});

function renderizarGraficoTempUmidade(dadosTemp, dadosUmidade) {
  const options = {
    series: [
      { name: 'Temperatura (°C)', type: 'line', data: dadosTemp },
      { name: 'Umidade (%)', type: 'area', data: dadosUmidade }
    ],
    chart: {
      height: 380,
      type: 'line',
      zoom: { enabled: true },
      foreColor: '#FFFFFF'
    },
    stroke: { width: [3, 1], curve: 'smooth' },
    fill: { opacity: [1, 0.25] },
    colors: ['#FF4560', '#008FFB'],
    xaxis: {
      type: 'datetime',
      labels: {
        datetimeUTC: false,
        format: 'dd/MM HH:mm'
      }
    },
    yaxis: [
      {
        title: { text: 'Temperatura (°C)' },
        labels: { formatter: (val) => val.toFixed(1) + ' °C' }
      },
      {
        opposite: true,
        title: { text: 'Umidade (%)' },
        labels: { formatter: (val) => val.toFixed(0) + ' %' }
      }
    ],
    tooltip: { x: { format: 'dd/MM/yyyy HH:mm:ss' } }
  };

  const chart = new ApexCharts(document.querySelector("#chart-temp-umidade"), options);
  chart.render();
}

function renderizarGraficoPressao(dadosPressao) {
  const options = {
    series: [{ name: 'Pressão (hPa)', data: dadosPressao }],
    chart: { height: 280, type: 'line', foreColor: '#FFFFFF'},
    colors: ['#775DD0'],
    xaxis: { type: 'datetime' },
    yaxis: {
      min: 945,
      max: 960,
      title: { text: 'hPa' }
    }
  };

  const chart = new ApexCharts(document.querySelector("#chart-pressao"), options);
  chart.render();
}

function renderizarGraficoDispersao(dadosDispersao) {
  const options = {
    series: [{
      name: 'Umidade vs Temperatura',
      data: dadosDispersao
    }],
    chart: {
      height: 350,
      type: 'scatter',
      zoom: { type: 'xy' },
      background: 'transparent',
      foreColor: '#FFFFFF'
    },
    theme: { mode: 'dark' },
    colors: ['#00E396'],
    xaxis: {
      title: { text: 'Temperatura (°C)' },
      tickAmount: 10,
      labels: { formatter: (val) => parseFloat(val).toFixed(1) }
    },
    yaxis: {
      title: { text: 'Umidade (%)' }
    }
  };

  const chart = new ApexCharts(document.querySelector("#chart-dispersao"), options);
  chart.render();
}

function renderizarGraficoEventos(dadosLuz, dadosChuva) {
  const options = {
    series: [
      { name: 'Luminosidade (Sol)', data: dadosLuz },
      { name: 'Ocorrência de Chuva', data: dadosChuva }
    ],
    chart: {
      height: 350,
      type: 'line', // Tipo linha com alteração no 'stroke' abaixo
      background: 'transparent',
      foreColor: '#FFFFFF'
    },
    theme: { mode: 'dark' },
    stroke: {
      curve: 'stepline', // Cria o efeito de "degrau" entre 0 e 1
      width: 2
    },
    colors: ['#FEB019', '#008FFB'], // Amarelo para luz, azul para chuva
    xaxis: {
      type: 'datetime',
      labels: { datetimeUTC: false, format: 'dd/MM' }
    },
    yaxis: {
      min: 0,
      max: 1.2, // Um pouco acima de 1 para dar margem visual no topo
      tickAmount: 1,
      labels: {
        formatter: (val) => {
          if (val === 0) return 'Não';
          if (val === 1) return 'Sim';
          return '';
        }
      }
    },
    dataLabels: { enabled: false },
    tooltip: { x: { format: 'dd/MM/yyyy HH:mm' } }
  };

  const chart = new ApexCharts(document.querySelector("#chart-eventos"), options);
  chart.render();
}