import {
    formatCNPJ,
    formatCPF,
    formatCPFOrCNPJ,
    formatDate,
    formatDocumentHierarchy,
    formatMPRJ,
    formatPropString,
    formatVehiclePlate,
    getNodeType,
} from '/static/js/utils.js'

const sidebarLeft = document.getElementById("entitylist")

/**
 *
 * @param {Object[]} nodes Array of nodes to be sorted
 * @param {String} type The type of node (which varies the key to sort them)
 */
const sortByType = (nodes, type) => {
    switch (type) {
        case 'pessoa':
            return sortByProperty(nodes, 'nome')
        case 'empresa':
            return sortByProperty(nodes, 'razao_social')
        case 'multa':
            return sortByProperty(nodes, 'data')
        default:
            return nodes
    }
}

/**
 * Sorts a node Array
 * @param {Object[]} nodes Array of nodes to be sorted
 * @param {Object} nodes[].properties
 * @param {Object} nodes[].properties.prop A number of string to be sorted.
 * @param {String} prop The name of the property to sort.
 */
const sortByProperty = (nodes, prop) => {
    return nodes.sort((a, b) => (a.properties[prop] > b.properties[prop]) ? 1 : -1)
}

/**
 * Returns a DOM string for a node on the sidebar
 * @param {Object} node
 * @param {Object} node.properties
 * @param {String[]} node.type
 */
const nodeToDOMString = node => {
    let ret = ''
    if (node) {
        switch (getNodeType(node)) {
            case 'documento':
                ret = `<dt onclick="zoomToNodeId(${node.id})">${formatMPRJ(node.properties.nr_mp)}</dt><dd>${formatDate(node.properties.dt_cadastro)} - ${formatDocumentHierarchy(node.properties.cldc_ds_hierarquia)}</dd>`
                break
            case 'embarcacao':
                ret = `<dt onclick="zoomToNodeId(${node.id})">${node.properties.nome_embarcacao}</dt>`
                break
            case 'empresa':
                console.log('este node', node)
                ret = `<dt onclick="zoomToNodeId(${node.id})">${node.properties.nome_fantasia || node.properties.razao_social}</dt><dd>CNPJ: ${formatCNPJ(node.properties.num_cnpj)}</dd>`
                break
            case 'multa':
                ret = `<dt onclick="zoomToNodeId(${node.id})">${formatDate(node.properties.datainfra)} - ${node.properties.descinfra}</dt>`
                break
            case 'orgao':
                ret = `<dt onclick="zoomToNodeId(${node.id})">${node.properties.nm_orgao}</dt>`
                break
            case 'pessoa':
                ret = `<dt onclick="zoomToNodeId(${node.id})">${node.properties.nome}</dt>`
                if (node.properties.cpf) {
                    ret += `<dd>CPF: ${formatCPF(node.properties.num_cpf)}</dd>`
                }
                break
            case 'personagem':
                ret = `<dt onclick="zoomToNodeId(${node.id})">${node.properties.pess_nm_pessoa} - ${node.properties.tppe_descricao}</dt><dd>CPF: ${formatCPFOrCNPJ(node.properties.cpfcnpj)}</dd>`
                break
            case 'veiculo':
                ret = `<dt onclick="zoomToNodeId(${node.id})">${node.properties.marca_modelo.trim()} ${node.properties.fabric}/${node.properties.modelo} ${node.properties.descricao_cor.trim()} - ${formatVehiclePlate(node.properties.placa)}</dt>`
                break
            default:
                ret = `<dt onclick="zoomToNodeId(${node.id})">${node.id}</dt>`
        }
    }
    return ret
}

/**
 * Updates left sidebar with entities to zoom
 * @param {String[]} labels Labels list
 * @param {Object[]} nodesData Nodes properties list
 */
export const updateLeftSidebar = (labels, nodesData) => {
    document.querySelector('.entitylist').style.display = 'block'
    let entityListToWrite = ''

    labels.sort().forEach(type => {
        type = type.toLowerCase()
        let nodesForThisType = sortByType(nodesData.filter(node => getNodeType(node) === type), type)
        if (nodesForThisType.length) {
            entityListToWrite += `
                <h2>
                    <a data-toggle='collapse' href='#collapse-${type}' role='button' class='color-${type}'>> ${formatPropString(type)}</a>
                </h2>
                <dl class='collapse in' id='collapse-${type}'>
            `
            nodesForThisType.forEach(node => {
                entityListToWrite += nodeToDOMString(node)
            })
            entityListToWrite += `</dl>`
        }
    })

    sidebarLeft.innerHTML = entityListToWrite
}
