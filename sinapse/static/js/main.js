const init = () => {
    initNeo4JD3()
    getLabels()
    initSearch()
}

let neo4jd3

let doubleClickTime = 0;
const threshold = 200;

const initNeo4JD3 = () => {
    neo4jd3 = new Neo4jd3('#neo4jd3', {
        highlight: [
            {
                class: 'Project',
                property: 'name',
                value: 'neo4jd3'
            }, {
                class: 'User',
                property: 'userId',
                value: 'eisman'
            }
        ],
        icons: {
            'Api': 'gear',
            'Cookie': 'paw',
            'Email': 'at',
            'Git': 'git',
            'Github': 'github',
            'Google': 'google',
            'Ip': 'map-marker',
            'Issues': 'exclamation-circle',
            'Language': 'language',
            'Options': 'sliders',
            'Password': 'lock',
            'Phone': 'phone',
            'Project': 'folder-open',
            'SecurityChallengeAnswer': 'commenting',
            'pessoa': 'user',
            'personagem':'users',
            'veiculo': 'car',
            'empresa': 'building',
            'mgp':'balance-scale',
            'zoomFit': 'arrows-alt',
            'zoomIn': 'search-plus',
            'zoomOut': 'search-minus'
        }, 
        images: {
            'Address': 'img/twemoji/1f3e0.svg',
            'BirthDate': 'img/twemoji/1f382.svg',
            'Cookie': 'img/twemoji/1f36a.svg',
            'CreditCard': 'img/twemoji/1f4b3.svg',
            'Device': 'img/twemoji/1f4bb.svg',
            'Email': 'img/twemoji/2709.svg',
            'Git': 'img/twemoji/1f5c3.svg',
            'Github': 'img/twemoji/1f5c4.svg',
            'icons': 'img/twemoji/1f38f.svg',
            'Ip': 'img/twemoji/1f4cd.svg',
            'Issues': 'img/twemoji/1f4a9.svg',
            'Language': 'img/twemoji/1f1f1-1f1f7.svg',
            'Options': 'img/twemoji/2699.svg',
            'Password': 'img/twemoji/1f511.svg',
            'Project': 'img/twemoji/2198.svg',
            'Project|name|neo4jd3': 'img/twemoji/2196.svg',
            'User': 'img/twemoji/1f600.svg'
        },
        minCollision: 60,
        neo4jDataUrl: '/static/json/neo4jData.json',
        nodeRadius: 25,
        onNodeDoubleClick: function(node) {
            doubleClickTime = new Date();
            get('api/nextNodes?node_id=' + node.id, (data) => {
                neo4jd3.updateWithNeo4jData(data)
            });                        
        },
        onRelationshipDoubleClick: function(relationship) {
            console.log('double click on relationship: ' + JSON.stringify(relationship))
        },
        onNodeClick: function(node) {
            let t0 = new Date();
            if (t0 - doubleClickTime > threshold) {
                setTimeout(function () {
                    if (t0 - doubleClickTime > threshold) {
                        populateSidebarRight(node);
                        showSidebarRight();
                    }
                },threshold);
            }
            
        },
        //zoomFit: true
    })
}

const getLabels = () => {
    get('/api/labels', setLabels)
}

const setLabels = labels => {
    let selectLabel = document.getElementById('selectLabel')

    // attach onchange event
    selectLabel.onchange = updateProps
    
    // remove children option
    while (selectLabel.firstChild) {
        selectLabel.removeChild(selectLabel.firstChild);
    }
    
    // add empty option
    let emptyOption = document.createElement('option')
    emptyOption.value = ''
    emptyOption.innerHTML = 'Escolha um tipo'
    selectLabel.appendChild(emptyOption)
    
    // add options
    labels.sort().map(label => appendOption(selectLabel, label))
}

const appendOption = (select, optionValue) => {
    var option = document.createElement('option')
    option.value = optionValue
    option.innerHTML = formatPropString(optionValue)
    select.appendChild(option)
}

const updateProps = () => {
    let label = document.getElementById('selectLabel').value
    getNodeProperties(label)
}

const getNodeProperties = label => {
    get(`api/nodeProperties?label=${label}`, setProps)

    // show loading
    let selectProp = document.getElementById('selectProp')
    while (selectProp.firstChild) {
        selectProp.removeChild(selectProp.firstChild);
    }
    let emptyOption = document.createElement('option')
    emptyOption.value = ''
    emptyOption.innerHTML = 'Aguarde, carregando...'
    selectProp.appendChild(emptyOption)
}

const setProps = nodeProperties => {
    let props = nodeProperties.data[0][0]
    
    let selectProp = document.getElementById('selectProp')
    
    // remove children option
    while (selectProp.firstChild) {
        selectProp.removeChild(selectProp.firstChild);
    }

    // add empty option
    let emptyOption = document.createElement('option')
    emptyOption.value = ''
    emptyOption.innerHTML = 'Escolha uma propriedade'
    selectProp.appendChild(emptyOption)
    
    // add options
    props.sort().map(prop => appendOption(selectProp, prop))
}

const initSearch = () => {
    document.getElementById('buttonBusca').onclick = findNodes
}

const findNodes = () => {
    let label = document.getElementById('selectLabel').value
    let prop = document.getElementById('selectProp').value
    let val = document.getElementById('textVal').value
    if (!label || !prop || !val) {
        return alert('ERRO: É preciso escolher o tipo, a propriedade e preencher um valor para realizar uma busca.')
    }
    get(`/api/findNodes?label=${label}&prop=${prop}&val=${val}`, updateNodes)
}

const updateNodes = data => {
    neo4jd3.updateWithNeo4jData(data)
}

/**
 * Adds diacritics (a => á) and formats props case.
 * 
 * @param {string} text The prop string to be formatted
 */
const formatPropString = text => {
    switch (text) {
        // 1st Level
        case 'veiculo':
            return 'Veículo'
        case 'orgao':
            return 'Órgão'
        case 'mgp':
            return 'MGP'
        // Empresa
        case 'cnae':
            return 'CNAE'
        case 'cnpj':
            return 'CNPJ'
        case 'cpf_responsavel':
            return 'CPF do Responsável'
        case 'data_inicio':
            return 'Data de Início'
        case 'municipio':
            return 'Município'
        case 'nome_responsavel':
            return 'Nome do Responsável'
        case 'razao_social':
            return 'Razão Social'
        case 'uf':
            return 'UF'
        // MGP
        case 'cdorgao':
            return 'Código do Órgão'
        case 'docu_dk':
            return 'ID do Documento'
        case 'dt_cadastro':
            return 'Data do Cadastro'
        case 'nr_ext':
            return 'Número Externo'
        case 'nr_mprj':
            return 'Número MPRJ'
        // Multa
        case 'desc':
            return 'Descrição'
        // Órgão
        case 'craai':
            return 'CRAAI'
        case 'dt_criacao':
            return 'Data de Criação'
        case 'dt_extincao':
            return 'Data de Extinção'
        case 'sensivel':
            return 'Sensível'
        case 'situacao':
            return 'Situação'
        // Pessoa
        case 'cpf':
            return 'CPF'
        case 'dt_nasc':
            return 'Data de Nascimento'
        case 'nome_mae':
            return 'Nome da Mãe'
        // Telefone
        case 'numero':
            return 'Número'
        // Veículo
        case 'cpfcnpj':
            return 'CPF/CNPJ'
        default:
            return text.split('_').map(word => word.substr(0, 1).toUpperCase() + word.substr(1)).join(' ')
    }
}

/**
 * Make a HTTP GET call and returns the data.
 * 
 * @param {String} url - The URL to GET
 * @param {Function} callback - A function to be executed with the returned data.
 */
const get = (url, callback) => {
    var xmlhttp = new XMLHttpRequest()
    xmlhttp.open('GET', url, true)
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4) {
            if(xmlhttp.status == 200) {
                var obj = JSON.parse(xmlhttp.responseText)
                console.log(obj)
                if (callback) {
                    callback(obj)
                }
            }
        }
    };
    xmlhttp.send(null);
}

const sidebarRight = document.getElementById("sidebarRight")

/*
    cores: 
    pessoa: #00d1e2
    empresas: #51c881
    telefone: #324eb6
    personagens: #a176d1
    multas: #ff524e
    veiculos: #ff8b63
    orgãos: #ffb842
    mgp: #ab897f
*/

const populateSidebarRight = (node) => {
    console.log(node)
    switch (node.labels[0]) {
        case 'personagem':
            sidebarRight.setAttribute("class", 'personagem')
            break
        case 'pessoa':
            sidebarRight.setAttribute("class", 'pessoa')
            break
        case 'empresa':
            sidebarRight.setAttribute("class", 'empresa')
            break
        case 'telefone':
            sidebarRight.setAttribute("class", 'telefone')
            break
        case 'multa':
            sidebarRight.setAttribute("class", 'multa')
            break
        case 'veiculo':
            sidebarRight.setAttribute("class", 'veiculo')
            break
        case 'orgao':
            sidebarRight.setAttribute("class", 'orgao')
            break
        case 'mgp':
            sidebarRight.setAttribute("class", 'mgp')
            break

        default:
            sidebarRight.setAttribute("class", '')
            break
    }

    let dataContainerDiv = document.createElement("aside")

    while (sidebarRight.hasChildNodes()) {
        sidebarRight.removeChild(sidebarRight.firstChild);
    }

    let content = document.createElement("div")
    content.setAttribute("id", "content")
    Object.keys(node.properties).forEach(function(property) {
        
        let labelSpan = document.createElement("span")
        labelSpan.className = "sidebarRight-label"
        let labelContent = document.createTextNode(formatPropString(property))
        labelSpan.appendChild(labelContent)
        content.appendChild(labelSpan)

        let dataSpan = document.createElement("span")
        dataSpan.className = "sidebarRight-data"
        let dataContent = document.createTextNode(node.properties[property])
        dataSpan.appendChild(dataContent)
        content.appendChild(dataSpan)


        console.log(property, node.properties[property])
    });

    let closeButton = document.createElement("button")
    closeButton.addEventListener("click", (e) => hideSidebarRight(), false)
    let closeButtonText = document.createTextNode("X")
    closeButton.setAttribute("id", "closeSidebarRight")
    closeButton.appendChild(closeButtonText)
    content.appendChild(closeButton)

    sidebarRight.appendChild(content)


}

const showSidebarRight = () => {
    sidebarRight.style.display = "block"
}

const hideSidebarRight = () => {
    sidebarRight.style.display = "none"
}
window.onload = init
