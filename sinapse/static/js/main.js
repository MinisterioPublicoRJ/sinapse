/**
 * Init function called on window.onload.
 */
const init = () => {
    // initNeo4JD3()
    getLabels()
    initSearch()
    initFilter()
    initVisjs()
}

// Initial vars
let nodes,               // Visjs initialized nodes
    nodesData,           // Nodes array as is from API
    edges,               // Visjs initialized edges (path between nodes)
    edgesData,           // Edges array as is from API
    entityTypes,         // Entity types from API
    filteredEntityTypes, // Entity types we don't want on future API queries
    container,           // Visjs DOM element
    data,                // Object with nodes and edges
    options,             // Object that holds Visjs options
    network              // Visjs Network, linking container, data and options

const baseIconsPath = '/static/img/icon/graph/'
const sidebarRight = document.getElementById("sidebarRight")

const initVisjs = () => {
    // initialize everything as empty (we don't have data yet)
    nodesData = []
    edgesData = []
    filteredEntityTypes = []
    nodes = new vis.DataSet([])
    edges = new vis.DataSet([])
    container = document.getElementById('graph')
    data = { nodes, edges }
    options = {
        edges: {
            color: {
                inherit: 'from',
            },
        },
        interaction:{
            hover: true,
        },
        locale: 'pt-br',
        locales: {
            'pt-br': {
                del: 'Apagar nó selecionado',
                edit: 'Editar',
            },
        },
        manipulation: {
            addEdge: false,
            addNode: false,
            enabled: true,
        },
    }
    network = new vis.Network(container, data, options)
    
    // Don't change to arrow function (`this` wouldn't work)
    network.on('click', function(params) {
        const selectedNodeId = this.getNodeAt(params.pointer.DOM)
        if (selectedNodeId) {
            const selectedNode = nodesData.filter(node => node.id === selectedNodeId)[0]
            // console.log('click event, getNodeAt returns: ' + selectedNodeId)
            // console.log('selectedNode: ', selectedNode)
            populateSidebarRight(selectedNode)
            showSidebarRight()
        }
    })
    network.on('doubleClick', function(params) {
        const selectedNodeId = this.getNodeAt(params.pointer.DOM)
        if (selectedNodeId) {
            getNextNodes(selectedNodeId)
        }
    })
    network.on("oncontext", function(params) {
        container.oncontextmenu = () => false // Cancels right click menu
    })
}

/**
 * Gets 
 * @param {Number} nodeId A Node ID to fetch from API
 */
const getNextNodes = nodeId => {
    get(`/api/nextNodes?node_id=${nodeId}`, updateNodes)
}

/**
 * Gets labels from the API.
 */
const getLabels = () => {
    get('/api/labels', setLabels)
}

/**
 * Sets labels and create a DOM element for each of them. Also initializes buttons events.
 *
 * @param {String[]} labels An array of labels as strings.
 */
const setLabels = data => {
    // store it
    labels = data

    // hides loading
    document.getElementById('loading').className = 'hidden'
    if (!window.filtroInicial) {
        document.getElementById('step1').className = ''
    }
    // create labels dynamically
    let labelsMenu = document.getElementById('opcoes')
    labels.sort().map(label => {
        if (label !== 'teste') {
            // <span>
            let labelTooltipEl = document.createElement('span')
            let labelTooltipStr = document.createTextNode(formatPropString(label))
            labelTooltipEl.appendChild(labelTooltipStr)
            labelTooltipEl.className = 'tooltip'
            // <img>
            let labelImg = document.createElement('img')
            labelImg.setAttribute('src', `/static/img/icon/${label}.svg`)
            labelImg.dataset.label = label
            // <div>
            //   <img>
            //   <span/>
            // </div>
            let labelEl = document.createElement('div')
            labelEl.appendChild(labelImg)
            labelEl.appendChild(labelTooltipEl)
            labelEl.className = label
            labelEl.onclick = getNodeProperties
            // append to DOM
            labelsMenu.appendChild(labelEl)
        }
    })
    // init comece-aqui button
    let comeceAquiEl = document.getElementById('comece-aqui')
    let opcoesEl = document.getElementById('opcoes')
    comeceAquiEl.onclick = () => {
        if (opcoesEl.className === 'opcoes') {
            opcoesEl.className = 'opcoes hidden'
        } else {
            opcoesEl.className = 'opcoes'
        }
    }
    // step2 back button
    document.getElementById('step2img').onclick = e => {
        document.getElementById('step1').className = ''
        document.getElementById('step2').className = 'hidden'
        document.getElementById('textBusca').style = 'hidden'
    }
}

/**
 * Gets node properties from the API.
 *
 * @param {Element} e the clicked node DOM Element.
 */
const getNodeProperties = e => {
    let label = e.target.dataset.label
    document.getElementById('step2img').setAttribute('src', `/static/img/icon/${label}.svg`)
    document.getElementById('selectLabel').value = label
    document.getElementById('form-step2').className = label
    get(`api/nodeProperties?label=${label}`, setProps)
}

/**
 * Append an option to a given select.
 *
 * @param {string} optionValue The <option> value and innerHTML.
 */
const appendOption = optionValue => {
    var mylist = document.getElementById('selectProp');
    mylist.insertAdjacentHTML('beforeend', `
        <input type="radio" class="badgebox" name="test" id="` + optionValue + `" value="` + optionValue + `" onclick="checkRadio()">
        <label for="` + optionValue + `" class="btnRadio">
            <span class="txtButton">` + formatPropString(optionValue) + `</span>
            <label class="badge2">            
                <svg xmlns="http://www.w3.org/2000/svg"  class="cls" viewBox="0 0 18.91 18.91">
                    <path d="M17.64,4.71A9.31,9.31,0,0,0,14.2,1.27,9.21,9.21,0,0,0,9.45,0,9.2,9.2,0,0,0,4.71,1.27,9.31,9.31,0,0,0,1.27,4.71,9.2,9.2,0,0,0,0,9.45,9.21,9.21,0,0,0,1.27,14.2a9.31,9.31,0,0,0,3.44,3.44,9.2,9.2,0,0,0,4.74,1.27,9.21,9.21,0,0,0,4.75-1.27,9.31,9.31,0,0,0,3.44-3.44,9.21,9.21,0,0,0,1.27-4.75,9.2,9.2,0,0,0-1.27-4.74ZM15.59,8,8.9,14.7a.79.79,0,0,1-.57.23.78.78,0,0,1-.55-.23L3.32,10.24a.78.78,0,0,1-.22-.55.81.81,0,0,1,.22-.57L4.44,8A.79.79,0,0,1,5,7.78.76.76,0,0,1,5.55,8L8.33,10.8l5-5a.74.74,0,0,1,.55-.24.77.77,0,0,1,.56.24l1.12,1.1a.81.81,0,0,1,.22.57.76.76,0,0,1-.22.55Z"/>
                </svg>                        
            </label>
        </label>`);
}

/**
 * Sets node properties from the API.
 *
 * @param {Array.<string>} nodeProperties
 */
const setProps = nodeProperties => {
    
    // hide step1, show step2
    document.getElementById('step1').className = 'hidden'
    document.getElementById('step2').className = ''
    document.getElementById('textVal').value = null

    let props = nodeProperties.data[0][0]
    //Deleting fields from object to not shown to user
    delete props[4]
    delete props[6]
    
    let selectProp = document.getElementById('selectProp')
    
    // remove children option
    while (selectProp.firstChild) {
        selectProp.removeChild(selectProp.firstChild);
    }

    // add options
    props.sort().map(prop => appendOption(prop))
}

/**
 * Adds the events to initialize search: button click and Enter keypress.
 */
const initSearch = () => {
    // Step 1 Search button
    document.getElementById('buttonBusca').onclick = findNodes
    // Step 2 Input Search Enter Event
    document.getElementById('textVal').addEventListener('keypress', e => {
        let key = e.keyCode
        if (key === 13) { // 13 is enter
            findNodes()
        }
    })
    // Step 3 Clear Search button
    document.getElementById('clear').onclick = e => {
        // show search form
        document.getElementById('step1').className = ''
        document.getElementById('step3').className = 'hidden'
        // hide sidebar
        hideSidebarRight()
    }
}

const checkRadio = () => {
    document.getElementById('textVal').value = null
    document.getElementById('textBusca').style.display = 'block'
    document.getElementById("textVal").focus()
}

/**
 * Reads data from DOM to find nodes (label, prop and val)
 */
const findNodes = () => {
    let label = document.getElementById('selectLabel').value
    let prop = document.querySelector('input[name="test"]:checked').value
    let val = document.getElementById('textVal').value

    _findNodes(label, prop, val)
}

/**
 * Gets from API the nodes that match the given label, prop and val.
 *
 * @param {string} label
 * @param {string} prop
 * @param {string} val
 */
const _findNodes = (label, prop, val) => {
    if (!label || !prop || !val) {
        return alert('ERRO: É preciso escolher o tipo, a propriedade e preencher um valor para realizar uma busca.')
    }
    get(`/api/findNodes?label=${label}&prop=${prop}&val=${val}`, updateNodes)

    // hide form
    document.getElementById('step1').className = 'hidden'
    document.getElementById('step2').className = 'hidden'
}

/**
 * Returns a node type.
 *
 * @param {*} node 
 */
const getNodeType = node => {
    return node.labels[0]
}

const addColorToNode = node => {
    let color = '#7bb3ff'

    switch (node.type[0]) {
        case 'empresa':
            color = '#51c881'
            break
        case 'mgp':
            color = '#ab897f'
            break
        case 'multa':
            color = '#ff524e'
            break
        case 'orgao':
            color = '#ffb842'
            break
        case 'personagem':
            color = '#a176d1'
            break
        case 'pessoa':
            color = '#00d1e2'
            break
        case 'telefone':
            color = '#324eb6'
            break
        case 'veiculo':
            color = '#ff8b63'
            break
    }

    return {
        ...node,
        color,
    }
}

/**
 * Update nodes with given API data.
 *
 * @param {*} data Data from API data.
 */
const updateNodes = data => {
    // update graph. notice we only add non-existant nodes/edges - no duplicates are allowed.
    if (data.nodes) {
        for (node of data.nodes) {
            // check if this node already exists checking its id
            let filteredNode = nodesData.filter(n => n.id === node.id)
            if (filteredNode.length === 0) {
                // doesn't exist, add it
                let formattedNode = addColorToNode(node)
                nodesData.push(formattedNode)
                nodes.add(formattedNode)
            }
        }
    }
    if (data.edges) {
        for (edge of data.edges) {
            // the same for edges
            let filteredEdge = edgesData.filter(e => e.id === edge.id)
            if (filteredEdge.length === 0) {
                edgesData.push(edge)
                edges.add(edge)
            }
        }
    }

    // show back button
    document.getElementById('step3').className = ''
}

/**
 * Adds diacritics (a => á) and formats props case.
 *
 * @param {string} text The prop string to be formatted.
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
 * @param {String} url The URL to GET.
 * @param {Function} callback A function to be executed with the returned data.
 */
const get = (url, callback) => {
    var xmlhttp = new XMLHttpRequest()
    xmlhttp.open('GET', url, true)
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4) {
            if(xmlhttp.status == 200) {
                var obj = JSON.parse(xmlhttp.responseText)
                if (callback) {
                    callback(obj)
                }
            }
        }
    }
    xmlhttp.send(null)
}

/**
 * Populates Right Sidebar with data form a node.
 *
 * @param {Object} node A node from Neo4J.
 */
const populateSidebarRight = node => {

    // Deleting fields from object to not shown to user
    delete node.properties['filho_rel_status']
    delete node.properties['filho_rel_status_pai']

    let label = node.type[0]
    switch (label) {
        case 'personagem':
            sidebarRight.setAttribute('class', 'personagem')
            break
        case 'pessoa':
            sidebarRight.setAttribute('class', 'pessoa')
            break
        case 'empresa':
            sidebarRight.setAttribute('class', 'empresa')
            break
        case 'telefone':
            sidebarRight.setAttribute('class', 'telefone')
            break
        case 'multa':
            sidebarRight.setAttribute('class', 'multa')
            break
        case 'veiculo':
            sidebarRight.setAttribute('class', 'veiculo')
            break
        case 'orgao':
            sidebarRight.setAttribute('class', 'orgao')
            break
        case 'mgp':
            sidebarRight.setAttribute('class', 'mgp')
            break

        default:
            sidebarRight.setAttribute('class', '')
            break
    }

    while (sidebarRight.hasChildNodes()) {
        sidebarRight.removeChild(sidebarRight.firstChild);
    }

    let content = document.createElement('div')
    content.setAttribute('id', 'content')

    let headerSidebarRight = document.createElement('div')
    headerSidebarRight.setAttribute('class', 'header')
    content.appendChild(headerSidebarRight)

    let valuesContainer = document.createElement('div')
    valuesContainer.setAttribute('id', 'valuesContainer')

    Object.keys(node.properties).forEach(function(property) {

        let labelSpan = document.createElement('span')
        labelSpan.className = 'sidebarRight-label'
        let labelContent = document.createTextNode(formatPropString(property))
        labelSpan.appendChild(labelContent)
        valuesContainer.appendChild(labelSpan)

        let dataSpan = document.createElement('span')
        dataSpan.className = 'sidebarRight-data'
        let dataContent = document.createTextNode(node.properties[property])

        dataSpan.appendChild(dataContent)
        valuesContainer.appendChild(dataSpan)

        // console.log(property, node.properties[property])
    });

    let closeButton = document.createElement("button")
    closeButton.addEventListener("click", (e) => hideSidebarRight(), false)
    closeButton.setAttribute("id", "closeSidebarRight")
    content.appendChild(valuesContainer)
    content.appendChild(closeButton)

    sidebarRight.appendChild(content)
}

/**
 * Displays the Right Sidebar.
 */
const showSidebarRight = () => {
    sidebarRight.style.display = "block"
    document.getElementsByTagName('body')[0].className = 'showingSidebarRight'

}

/** Hides the Right Sidebar. */
const hideSidebarRight = () => {
    sidebarRight.style.display = "none"
    document.getElementsByTagName('body')[0].className = ''
}

/**
 * Initialize filter events
 */
const initFilter = () => {
    const filterExpanded = document.getElementById('filter-expanded')

    // Show/hide filter
    document.getElementById('filter-call').onclick = e => {
        if (filterExpanded.className) {
            filterExpanded.className = ''
        } else {
            filterExpanded.className = 'hidden'
        }
    }
    // Each filter
    document.querySelectorAll('.filter .entity').forEach(filter => {
        filter.onclick = e => {
            let entityType = filter.classList[1]
            if (filter.classList.contains('disabled')) {
                filter.classList.remove('disabled')
                filteredEntityTypes.splice(filteredEntityTypes.indexOf(entityType), 1)
            } else {
                filter.classList.add('disabled')
                filteredEntityTypes.push(entityType)
            }
            updateFilteredEntityTypes()
        }
    })
}

/**
 * Updates entities hidden status based on their types
 */
const updateFilteredEntityTypes = () => {
    // first make all hidden nodes visible
    let filteredNodes = []
    nodesData.filter(node => node.hidden).forEach(node => {
        filteredNodes.push({id: node.id, hidden: false})
        node.hidden = false
    })
    nodes.update(filteredNodes)

    // then hide nodes with filtered types
    filteredNodes = []
    filteredEntityTypes.forEach(type => {
        nodesData.filter(node => node.type[0] === type).forEach(node => {
            filteredNodes.push({id: node.id, hidden: true})
            node.hidden = true
        })
    })
    nodes.update(filteredNodes)
}

// Finally, declare init function to run when the page loads.
window.onload = init
