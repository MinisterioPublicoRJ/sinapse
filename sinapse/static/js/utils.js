/**
 * Format as CNAE - xxxx-x/xx
 * @param {String} cnae
 */
export const formatCNAE = cnae => {
    return `${cnae.substr(0,4)}-${cnae.substr(4,1)}/${cnae.substr(5)}`
}

/**
 * Formats as CNPJ - xx.xxx.xxx/xxxx-xx
 * @param {String} cnpj
 */
export const formatCNPJ = cnpj => {
    if (cnpj.length === 14) {
        return `${cnpj.substr(0,2)}.${cnpj.substr(2,3)}.${cnpj.substr(5,3)}/${cnpj.substr(8,4)}-${cnpj.substr(12)}`
    }
    return cnpj
}

/**
 * Formats as CPF - xxx.xxx.xxx-xx
 * @param {String} cpf
 */
export const formatCPF = cpf => {
    cpf = cpf.toString().padStart(11, "0")
    if (cpf.length === 11) {
        return `${cpf.substr(0,3)}.${cpf.substr(3,3)}.${cpf.substr(6,3)}-${cpf.substr(9)}`
    }
    return cpf
}

/**
 * Formats as Date - from yyyymmdd to dd/mm/yyyy
 * @param {String} date
 */
export const formatDate = date => {
    if (date.length === 8) {
        return `${date.substr(6,2)}/${date.substr(4,2)}/${date.substr(0,4)}`
    }
    return `${date.substr(8,2)}/${date.substr(5,2)}/${date.substr(0,4)}`
}

/**
 * Formats Gender string
 * @param {String} genderId
 */
export const formatGender = genderId => {
    switch (genderId) {
        case "1":
            return "Masculino"
        case "2":
            return "Feminino"
        default:
            return genderId
    }
}

/**
 * Format RG on Detran format - xx.xxx.xxx-x
 * @param {String} rg
 */
export const formatRG = rg => {
    if (rg.length === 9) {
        return `${rg.substr(0,2)}.${rg.substr(2,3)}.${rg.substr(5,3)}-${rg.substr(-1)}`
    }
    return rg
}

/**
 * Format Vehicle Ident as CPF or CNPJ
 * @param {String} ident Vehicle owner ident
 */
export const formatVehicleIdent = ident => {
    // ident is the PK of vehicle owner, either CPF or CNPJ
    // we will naively assume that if it starts with three zeroes, its a CPF, otherwise, it should be a CNPJ
    if (ident.substr(0,3) === '000') {
        return formatCPF(ident.substr(3))
    }
    formatCNPJ(ident)
}

/**
 * Format as Vehicle Plate - XXX-XXXX
 * @param {string} plate
 * @return {string}
 */
export const formatVehiclePlate = plate => {
    if (plate.length === 7) {
        return `${plate.substr(0,3)}-${plate.substr(3)}`
    }
    return plate
}

/**
 * Formats number with thousands separators - NNNNN => NN.NNN
 * @param {string|number} num number to be formatted
 * @returns {string}
 */
export const thousandsSeparator = num => {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')
}