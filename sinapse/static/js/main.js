import {
    addStyleToNode,
    formatKeyString,
    formatPropString,
    formatAddresses,
    get,
    getCardTitle,
    getNodeType,
    sanitizeQuery,
    showLoading,
    hideLoading,
    thousandsSeparator,
} from '/static/js/utils.js'
import { entityCard } from '/static/js/cards.js'
import { updateLeftSidebar } from '/static/js/entitylist.js'

/**
 * Init function called on window.onload.
 */
const init = () => {
    getLabels()
    initSearch()
    initFilter()
    initVisjs()
    initVersion()
}

const VERSION = '20190501'

// Initial vars
let nodes,               // Visjs initialized nodes
    nodesData,           // Nodes array as is from API
    edges,               // Visjs initialized edges (path between nodes)
    edgesData,           // Edges array as is from API
    searchData,          // Data last returned by search API
    filteredEntityTypes, // Entity types we don't want on future API queries
    container,           // Visjs DOM element
    data,                // Object with nodes and edges
    options,             // Object that holds Visjs options
    network,             // Visjs Network, linking container, data and options
    photosData,
    labels

const baseIconsPath = '/static/img/icon/graph/'
const sidebarRight = document.getElementById("sidebarRight")

const initVisjs = () => {
    // initialize everything as empty (we don't have data yet)
    nodesData = []
    edgesData = []
    photosData = {}
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
        nodes: {
            chosen: {
                node(values) {
                    values.borderWidth = 10
                    values.size = 30
                },
            },
        },
        physics: {
            solver: 'forceAtlas2Based',
            stabilization: {
                enabled: true,
                iterations: 1000,
                updateInterval: 25
            },
        },
    }
    network = new vis.Network(container, data, options)
    
    // Don't change to arrow function (`this` wouldn't work)
    network.on('click', function(params) {
        const selectedNodeId = this.getNodeAt(params.pointer.DOM)
        if (selectedNodeId) {
            const selectedNode = nodesData.filter(node => node.id === selectedNodeId)[0]
            console.log(selectedNode)
            populateSidebarRight(selectedNode)
            showSidebarRight()
        } else {
            emptySidebarRight()
            hideSidebarRight()
        }
    })
    network.on('doubleClick', function(params) {
        const selectedNodeId = this.getNodeAt(params.pointer.DOM)
        if (selectedNodeId) {
            getNextNodes(selectedNodeId)
        }
    })
    network.on('oncontext', function(params) {
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
    hideLoading()

    // displays search
    document.querySelector('#search-area').className = ''
}

/**
 * Initialize search
 */
const initSearch = () => {
    document.getElementById('form-search-area').addEventListener('submit', e => {
        e.preventDefault()
        showLoading()
        document.querySelector('#search-result').innerHTML = ''
        get(`/api/search?q=${sanitizeQuery(e.target[0].value)}`, searchCallback)
    })
}

/**
 * Creates tabs for entity search
 * @param {*} data The whole data returned from API, to get highlight information
 * @param {bool} bondSearchId whether the card is being called within the bond search list result or in the main search screen
*/
const createSearchTabs = (data, bondSearchId) => {
    let finalHTML = '<ul class="nav nav-tabs" role="tablist">'

    // first it iterates each 'object_type' (empresa, pessoa, veiculo) to create tabs
    Object.keys(data).forEach((key, index) => {
        let tabLink = bondSearchId ? `bond_${key}` : key
        finalHTML += `<li role="presentation" ${index === 1 ? 'class="active"' : ''}>
            <a href="#${tabLink}" role="tab" class="custom-tab ${key}" data-toggle="tab">
                <img src="/static/img/icon/${key}.svg" />
                <p class="number color-${key}">${thousandsSeparator(data[key].response.numFound)}</p>
                <p class="color-${key}">${key}${data[key].response.numFound > 1 ? 's' : ''}</p>
            </a>
        </li>`
    })

    finalHTML += '</ul>'
    return finalHTML
}

/**
 * Creates cards with entity search results
 * @param {*} data The whole data returned from API, to get highlight information
 * @param {bool} bondSearchId whether the card is being called within the bond search list result or in the main search screen
*/
const createSearchCards = (data, bondSearchId) => {
    let finalHTML = '<div class="tab-content">'

    // then, for each 'object_type', create a tab panel
    Object.keys(data).forEach((key, indexKey) => {
        let tabId = bondSearchId ? `bond_${key}` : key
        finalHTML += `<div role="tabpanel" class="tab-pane ${indexKey === 1 ? 'active' : ''} ${key}" id="${tabId}">`
        // and for each 'doc', create a card
        data[key].response.docs.forEach(doc => {
            finalHTML += entityCard(doc, key, data, false, bondSearchId)
        })
        // treat empty result
        if (data[key].response.docs.length === 0) {
            finalHTML += '<p>Não há resultados para este tipo de entidade para o valor pesquisado.'
        }
        finalHTML += '</div>'
    })
    finalHTML += '</div>'

    return finalHTML
}

/**
 * Creates entity search result
 * @param {*} data The whole data returned from API, to get highlight information
 * @param {Number} bondSearchId whether the card is being called within the bond search list result or in the main search screen
*/
const createSearchContent = (data, bondSearchId) => createSearchTabs(data, bondSearchId) + createSearchCards(data, bondSearchId)

/**
 * Function called when search call is returned from API
 * @param {Object} data data from API
 * @param {Object} data.object_type objects of a given type that matches this search term. currently supported are: empresa, pessoa, veiculo
 * @param {Object} data.object_type.highlighting highlighted terms returned by search
 * @param {Object} data.object_type.highlighting.uuid a object that has a highlighted term
 * @param {String[]} data.object_type.highlighting.uuid.prop the terms that matches the searched term
 * @param {Object} data.object_type.response the data that matches the searched term
 * @param {Object[]} data.object_type.response.docs each matched object data (entity)
 * @param {Number} data.object_type.respose.numFound the quantity of items matching this search
 * @param {Number} data.object_type.response.start first item, should be 0 unless making pagination
 */
const searchCallback = data => {
    hideLoading()
    searchData = data
    document.querySelector('#balls-animation').style.display = 'none'
    document.querySelector('#search-result').innerHTML = createSearchContent(data)
}

const addVeiculoFoto = data => {
    console.log(data)
}

const backToSearch = () => {
    document.querySelector('#search-area').style.display = 'block'
    document.querySelector('#search-result').style.display = 'block'
    document.querySelector('#search-details').style.display = 'none'
}

const searchDetailStep = (entityUUID, entityType) => {
    document.querySelector('#search-area').style.display = 'none'
    document.querySelector('#search-result').style.display = 'none'
    document.querySelector('#search-details').style.display = 'block'
    let searchedDoc = searchData[entityType].response.docs.filter(doc => doc.uuid === entityUUID)[0]
    console.log(entityUUID, entityType, searchedDoc)

    let searchDetailsHTML = `<div class="${entityType}">
        ${entityCard(searchedDoc, entityType, searchData, true)}
        <div class="col-lg-4 action busca-paradeiro" onclick="searchWhereabouts('${entityUUID}')">
            Busca<br>
            <b>Paradeiro</b>
        </div>
        <div class="col-lg-4 action caminho-exploratorio" onclick="showEntity('${searchedDoc.label}', '${entityUUID}')">
            Caminho<br>
            <b>Exploratório</b>
        </div>
        <div class="col-lg-4 action analise-de-vinculos" onclick="bondAnalysis('${entityUUID}','${entityType}','${searchedDoc[getCardTitle(entityType)]}')">
            Análise de<br>
            <b>Vínculos</b>
        </div>
    </div>`

    document.querySelector('#search-details').innerHTML = searchDetailsHTML
}

/**
 * Gets from API the nodes that match the given label, prop and val.
 *
 * @param {string} label
 * @param {string} prop
 * @param {string} val
 */
const findNodes = (label, prop, val) => {
    if (!label || !prop || !val) {
        return alert('ERRO: É preciso escolher o tipo, a propriedade e preencher um valor para realizar uma busca.')
    }
    get(`/api/findNodes?label=${label}&prop=${prop}&val=${val}`, updateFromFindNodes)
}

/**
 * Call getNextNodes on node returned by findNodes, so the graph comes already expanded on first level (instead of a single node)
 * @param {Object} data 
 * @param {Object[]} data.nodes
 * @param {String} data.nodes[].id
 */
const updateFromFindNodes = data => {
    if (data.nodes[0]) {
        getNextNodes(data.nodes[0].id)
    }
}

/**
 * Update nodes with given API data.
 *
 * @param {*} data Data from API data.
 */
const updateNodes = data => {
    document.querySelector('.busca').style.display = 'none'
    document.querySelector('footer').className = ''
    document.querySelector('#graph').className = ''
    // update graph. notice we only add non-existant nodes/edges - no duplicates are allowed.
    if (data.nodes) {
        for (let node of data.nodes) {
            // check if this node already exists checking its id
            let filteredNode = nodesData.filter(n => n.id === node.id)
            if (filteredNode.length === 0) {
                // doesn't exist, add it
                let formattedNode = addStyleToNode(node)
                nodesData.push(formattedNode)
                nodes.add(formattedNode)
            }
            // if it's a person or vehicle, check if we can add it to our photos array
            let nodeType = getNodeType(node)
            if (
                (
                    (nodeType === 'pessoa' && node.properties.rg) ||
                    (nodeType === 'veiculo')
                )
                && !photosData[node.uuid]
            ) {
                let imageEndpoint
                switch (nodeType) {
                    case 'pessoa':
                        imageEndpoint = `/api/foto?rg=${node.properties.rg}`
                        break;
                    case 'veiculo':
                        imageEndpoint = `/api/foto-veiculo?caracteristicas=${node.properties.marca_modelo} ${node.properties.modelo} ${node.properties.descricao_cor}`
                        break;
                }
                get(imageEndpoint, data => {
                    if (data.uuid && data.imagem) {
                        if (!photosData[data.uuid]) {
                            photosData[data.uuid] = data
                            nodes.update({id: data.uuid, shape: 'circularImage', image: `data:image/png;base64,${data.imagem}`})
                        }
                    }
                })
            }
        }
    }
    if (data.edges) {
        for (let edge of data.edges) {
            // the same for edges
            let filteredEdge = edgesData.filter(e => e.id === edge.id)
            if (filteredEdge.length === 0) {
                if (edge.label) {
                    edge.label = edge.label.toLowerCase()
                    // fix diacritics
                    switch (edge.label) {
                        case 'orgao_responsavel':
                            edge.label = 'órgão responsável'
                        case 'proprietario':
                            edge.label = 'proprietário'
                            break
                    }
                }
                edgesData.push(edge)
                edges.add(edge)
            }
        }
    }

    // show back button
    document.getElementById('step4').className = ''

    updateLeftSidebar(labels, nodesData)
}

/**
 * Zooms to a given nodeId
 * @param {String} nodeId
 */
const zoomToNodeId = nodeId => {
    network.focus(nodeId, { scale: 2, animation: true })
    const selectedNode = nodesData.filter(node => node.id === nodeId.toString())[0] // nodeId comes as Number, node.id is a String
    populateSidebarRight(selectedNode)
    showSidebarRight()
    network.selectNodes([nodeId.toString()])
}

const emptySidebarRight = () => {
    while (sidebarRight.hasChildNodes()) {
        sidebarRight.removeChild(sidebarRight.firstChild)
    }
}

/**
 * Populates Right Sidebar with data form a node.
 *
 * @param {Object} node A node from Neo4J.
 */
const populateSidebarRight = node => {
    sidebarRight.setAttribute('class', getNodeType(node))

    emptySidebarRight()

    let html = `<div id="content">
        <div class="header bgcolor-${getNodeType(node)}">`
    // Add person photo
    let nodeType = getNodeType(node)
    if (
        (
            (nodeType === 'pessoa' && node.properties.rg) ||
            (nodeType === 'veiculo')
        )
        && photosData[node.id]
    ) {
        html += `<img src="data:image/png;base64,${photosData[node.id].imagem}">`
    }
    html += `</div>
    <div id="valuesContainer">`
    Object.keys(node.properties).forEach(property => {
        if (
            property === 'filho_rel_status' ||
            property === 'filho_rel_status_pai' ||
            property === 'uuid' ||
            property.substr(0,1) === '_' ||
            property.substr(-3) === '_dk'
        ) {
            return // skip this property
        }

        html += `<span class="sidebarRight-label">${formatPropString(property)}</span>
        <span class="sidebarRight-data color-${nodeType}">${formatKeyString(property, node.properties[property])}</span>`
    });
    html += `</div>
        <button id="closeSidebarRight" class="color-${nodeType}" onclick="hideSidebarRight()"></button>
        <button id="fullSidebarRight" onclick="fullSidebarRight()"></button>
    </div>`

    sidebarRight.innerHTML = html
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
    document.getElementById('sidebarRight').style.display = "none"
    sidebarRight.style.display = "none"
    document.getElementsByTagName('body')[0].className = ''
}

/** Full/Hide the Right Sidebar. */
const fullSidebarRight = () => {
    var x = document.getElementById("sidebarRight");
    if (x.style.width === "") {
        x.style.width = "100%";
    } else if (x.style.width === "0%") {
        x.style.width = "100%";
    } else {
        x.style.width = "0%";
    }
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
        nodesData.filter(node => getNodeType(node) === type).forEach(node => {
            filteredNodes.push({id: node.id, hidden: true})
            node.hidden = true
        })
    })
    nodes.update(filteredNodes)
}

/**
 * Shows build information
 */
const initVersion = () => {
    document.getElementById('version_number').innerHTML = `Versão: ${VERSION}-${btoa(document.getElementById('version_username').innerHTML)}`
}

const showEntity = (entityType, uuid) => {
    console.log(`showEntity(${uuid})`)
    document.querySelector('.busca').style.display = 'none'
    findNodes(entityType, 'uuid', uuid)
}

const bondAnalysis = (nodeId1, nodeType1, nodeTitle1) => {
    document.querySelector('#search-details').style.display = 'none'
    let template = `
    <div class="row">
        <div class="col-lg-5 ${nodeType1} entity">
            <img src="/static/img/icon/${nodeType1}.svg"/>
            <input class="color-${nodeType1}" disabled value="${nodeTitle1}">
        </div>
        <div class="col-lg-2">
            <div class="add-bond">
                <img src="/static/img/icon/icon-vinculos.svg" />
            </div>
            <p class="text">
                Análise de <br />
                <b>Vínculos</b>
            </p>
        </div>
        <div id="bond-search" class="col-lg-5 entity entity-empty">
            <img src="/static/img/icon/vinculo-empty.svg"/>
            <form id="form-bond-search">
                <input class="color-veiculo" value="" placeholder="Procure um vínculo">
            </ form>
        </div>
    </div>
    <div class="row">
        <div class="col-lg-5"></div>
        <div class="col-lg-7">
            <div id="bond-search-result"></div>
        </div>
    </div>
    `
    document.querySelector('#bond-analysis').innerHTML = template
    document.getElementById('form-bond-search').addEventListener('submit', e => {
        e.preventDefault()
        showLoading()
        document.querySelector('#bond-search-result').innerHTML = ''
        get(`/api/search?q=${sanitizeQuery(e.target[0].value)}`, data => {
            bondSearchCallback(data, nodeId1)
        })
    })
}

const bondSearchCallback = (data, nodeId1) => {
    hideLoading()
    document.querySelector('#bond-search-result').innerHTML = createSearchContent(data, nodeId1)
}

const doBondSearch = (nodeId1, nodeId2) => {
    // getShortestPath(nodeId1, nodeId2)
    // hardcoded, falta interface
    getShortestPath(140885160, 81208568)
}

const getShortestPath = (nodeId1, nodeId2) => {
    get(`/api/findShortestPath?node_id1=${nodeId1}&node_id2=${nodeId2}`, updateNodes)
}

const searchWhereabouts = nodeId => {
    document.querySelector('#search-details').style.display = 'none'

    //get(`/api/whereabouts?node_id=${nodeId}`, displayWhereabouts)

    // hardcoded
    get(`/api/whereabouts?node_id=140885160`, displayWhereabouts)
    showLoading()
}

const displayWhereabouts = data => {
    hideLoading()
    console.log(data)

    let credilinkAddresses = data.filter(addresses => addresses.type === 'credilink')
    let receitaFederalAddresses = data.filter(addresses => addresses.type === 'receita_federal')

    document.querySelector('#whereabouts').innerHTML = `
        <div class="row pessoa">
            <div class="col-lg-2">(foto)</div>
            <div class="col-lg-5">
                <h3>Credilink</h3>
                ${formatAddresses(credilinkAddresses[0].formatted_addresses)}
            </div>
            <div class="col-lg-5">
                <h3>Receita Federal</h3>
                ${formatAddresses(receitaFederalAddresses[0].formatted_addresses)}
            </div>
        </div>
    `
}

// Attach external functions to window
window.addVeiculoFoto = addVeiculoFoto
window.backToSearch = backToSearch
window.bondAnalysis = bondAnalysis
window.doBondSearch = doBondSearch
window.findNodes = findNodes
window.fullSidebarRight = fullSidebarRight
window.hideSidebarRight = hideSidebarRight
window.searchDetailStep = searchDetailStep
window.searchWhereabouts = searchWhereabouts
window.showEntity = showEntity
window.zoomToNodeId = zoomToNodeId

// Finally, declare init function to run when the page loads.
window.onload = init
