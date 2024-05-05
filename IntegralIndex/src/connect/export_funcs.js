function export_build(self){
    let build = {}
    build = Object.assign(build, self.parametrs_of_build);
    return {"error": false, "result": build}
}

let export_funcs = {};
export_funcs.export_build = export_build


export default export_funcs