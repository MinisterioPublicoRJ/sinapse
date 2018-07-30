/**
 * Init function called on window.onload.
 */
const init = () => {
    initNeo4JD3()
    getLabels()
    initSearch()
    initFooter()
}

// Initial vars
let neo4jd3
let doubleClickTime = 0
const threshold = 200
const sidebarRight = document.getElementById("sidebarRight")
const clickedNodes = []

const checkNodeWasClicked = node => {
    for (nodeIndex in clickedNodes) {
        let clickedNode = clickedNodes[nodeIndex]
        if (clickedNode.id === node.id) {
            return true
        }
    }
    return false
}

const baseIconsPath = '/static/img/icon/graph/'

/**
 * Inits the Neo4JD3 graph.
 */
const initNeo4JD3 = () => {
    neo4jd3 = new Neo4jd3('#neo4jd3', {
        iconsPaths: {
            'empresa': baseIconsPath+'empresa.svg',
            'mgp':baseIconsPath+'mgp.svg',
            'multa':baseIconsPath+'multa.svg',
            'orgao':baseIconsPath+'orgao.svg',
            'pessoa': baseIconsPath+'pessoa.svg',
            'personagem':baseIconsPath+'personagem.svg',
            'telefone':baseIconsPath+'telefone.svg',
            'veiculo': baseIconsPath+'veiculo.svg',
        },
        infoPanel: false,
        minCollision: 80,
        neo4jDataUrl: '/static/json/neo4jData_vazio.json',
        nodeRadius: 25,
        onNodeDoubleClick: node => {
            doubleClickTime = new Date();

            if(checkNodeWasClicked(node)){
                return false
            }
            clickedNodes.push(node)
            get('api/nextNodes?node_id=' + node.id, data => {
                neo4jd3.updateWithNeo4jData(data)
                updateNodeSize()
            });
        },
        onRelationshipDoubleClick: relationship => {
            console.log('double click on relationship: ' + JSON.stringify(relationship))
        },
        onNodeClick: node => {
            let t0 = new Date()
            if (t0 - doubleClickTime > threshold) {
                setTimeout(function () {
                    if (t0 - doubleClickTime > threshold) {
                        if (node.labels[0] !== 'sigiloso') {
                            populateSidebarRight(node)
                            showSidebarRight()
                        }
                    }
                }, threshold)
            }
        },
    })
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
 * @param {Array.<string>} labels An array of labels as strings.
 */
const setLabels = labels => {
    document.getElementById('loading').className = 'hidden'
    if (!window.filtroInicial) {
        document.getElementById('step1').className = ''
    }
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
 * @param {Element} select The <select> DOMElement to append the created <option>
 * @param {string} optionValue The <option> value and innerHTML.
 */
const appendOption = (select, optionValue) => {
    var option = document.createElement('option')
    option.value = optionValue
    option.innerHTML = formatPropString(optionValue)
    select.appendChild(option)
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

    let props = nodeProperties.data[0][0]
    
    let selectProp = document.getElementById('selectProp')
    
    // remove children option
    while (selectProp.firstChild) {
        selectProp.removeChild(selectProp.firstChild);
    }

    // add empty option
    let emptyOption = document.createElement('option')
    emptyOption.value = ''
    emptyOption.innerHTML = 'Refinar a busca'
    selectProp.appendChild(emptyOption)
    
    // add options
    props.sort().map(prop => appendOption(selectProp, prop))
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
        // clear graph
        neo4jd3.clearNodes()
        // show search form
        document.getElementById('step1').className = ''
        document.getElementById('step3').className = 'hidden'
        // hide sidebar
        hideSidebarRight()
    }
}

/**
 * Gets from API the nodes that match the given label, prop and val.
 */
const findNodes = () => {
    let label = document.getElementById('selectLabel').value
    let prop = document.getElementById('selectProp').value
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
 * Updates Neo4JD3 created nodes' circles with different sizes for each node type.
 */
const updateNodeSize = () => {
    const largeRadius = 50
    const smallRadius = 20
    d3.select('svg').selectAll('circle').attr('r', d => {
        let nodeType = getNodeType(d)
        if (nodeType === "pessoa" || nodeType === "empresa") {
            return largeRadius
        }
        return smallRadius
    })

    d3.select('svg').selectAll('.relationship path').attr('fill', (d) => {
        let nodeType = getNodeType(d.target)

        if (nodeType === "pessoa" || nodeType === "empresa") {
            return "#000000"
        }
        return "#ededed"
    })

    d3.select('svg').selectAll('image')
        .attr('height', d => {
            let nodeType = getNodeType(d)
            if (nodeType === "pessoa" || nodeType === "empresa") {
                return largeRadius*2
            }
            return smallRadius*2
        })
        .attr('width', d => {
            let nodeType = getNodeType(d)
            if (nodeType === "pessoa" || nodeType === "empresa") {
                return largeRadius*2
            }
            return smallRadius*2
        })
        .attr('x', function(d) {
            let nodeType = getNodeType(d)
            if (nodeType === "pessoa" || nodeType === "empresa") {
                return `-${largeRadius}px`
            }
            return `-${smallRadius}px`
        })
        .attr('y', function(d) {
            let nodeType = getNodeType(d)
            if (nodeType === "pessoa" || nodeType === "empresa") {
                return `-${largeRadius}px`
            }
            return `-${smallRadius}px`
        })
}

/**
 * Returns a node type.
 *
 * @param {*} node 
 */
const getNodeType = node => {
    return node.labels[0]
}

/**
 * Update nodes with given Neo4J database.
 *
 * @param {*} data Data from Neo4J database.
 */
const updateNodes = data => {
    // update graph
    neo4jd3.updateWithNeo4jData(data)
    updateNodeSize()

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
    node.properties['sexo'] = node.properties['sexo'] == 1 ? 'Masculino' : 'Feminino'

    let label = node.labels[0]
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

        console.log(property, node.properties[property])
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
 * Initialize the footer click event.
 */
const initFooter = () => {
    const legendExpanded = document.getElementById('legend-expanded')
    document.getElementById('legend-call').onclick = e => {
        if (legendExpanded.className) {
            legendExpanded.className = ''
        } else {
            legendExpanded.className = 'hidden'
        }
    }
}

// Finally, declare init function to run when the page loads.
window.onload = init
