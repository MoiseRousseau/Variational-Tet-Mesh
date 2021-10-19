/* Var-Tet-Mesher: a simple variational tetrahedral mesher */



#include <geogram/basic/common.h>
#include <geogram/basic/logger.h>
#include <geogram/basic/command_line.h>
#include <geogram/basic/command_line_args.h>
#include <geogram/basic/progress.h>
#include <geogram/basic/stopwatch.h>
#include <geogram/basic/process.h>
#include <geogram/basic/file_system.h>
#include <geogram/basic/geometry_nd.h>

#include <geogram/mesh/mesh.h>
#include <geogram/mesh/mesh_io.h>
#include <geogram/mesh/mesh_tetrahedralize.h>

#include <geogram/voronoi/CVT.h>

#include <typeinfo>
#include <algorithm>

namespace {

    using namespace GEO;
    
    /**
     * \brief Generates a tetrahedral mesh.
     * \param[in] input_filename name of the input file, can be
     *   either a closed surfacic mesh or a tetrahedral mesh
     * \param[in] output_filename name of the output file
     * \retval 0 on success
     * \retval non-zero value otherwise
     */
    int tetrahedral_mesher(
        const std::string& input_filename, const std::string& output_filename
    ) {
        MeshIOFlags flags;
        flags.set_element(MESH_CELLS);

        Mesh M_in;
        Mesh M_tet; //for output
        if(!mesh_load(input_filename, M_in, flags)) {
            return 1;
        }
        M_tet.copy(M_in);
        
        
        if(M_in.cells.nb() == 0) {
            Logger::out("Pretet") << "Mesh is not a volume" << std::endl;
            Logger::out("Pretet") << "Autodetect enclosed volume "
                               << "and pretetrahedralize" << std::endl;
            if(!mesh_tetrahedralize(M_in)) {
                return 1;
            }
            M_in.cells.compute_borders();
        }
        
        Logger::div("Generate random samples");
        
        index_t dim = M_in.vertices.dimension();
        CentroidalVoronoiTesselation CVT(&M_in, coord_index_t(dim));
        CVT.set_volumetric(true);
	    
	    index_t nb_pts = CmdLine::get_arg_uint("remesh:nb_pts");
	    CVT.compute_initial_sampling(nb_pts);
	    
        double *p;
	    CVT.resize_points(M_in.vertices.nb() + nb_pts);
	    for (index_t v=0; v < M_in.vertices.nb(); v++) {
	        p = CVT.embedding(v+nb_pts);
            for (index_t c=0; c < 3; ++c) {
                *p = M_tet.vertices.point(v)[c];
                p++;
            }
	        CVT.lock_point(v+nb_pts);
	    }

	    Logger::div("Optimize sampling");

	    try {
		    index_t nb_iter = CmdLine::get_arg_uint("opt:nb_Lloyd_iter");
		    ProgressTask progress("Lloyd", nb_iter);
		    CVT.set_progress_logger(&progress);
		    CVT.Lloyd_iterations(nb_iter);
	    }
	    catch(const TaskCanceled&) {
	    }

	    try {
		    index_t nb_iter = CmdLine::get_arg_uint("opt:nb_Newton_iter");
		        ProgressTask progress("Newton", nb_iter);
		    CVT.set_progress_logger(&progress);
		    CVT.Newton_iterations(nb_iter);
	    }
	    catch(const TaskCanceled&) {
	    }
        
        
        Logger::div("Tetrahedralize");
        //remove tets from M_tet if 3D input
        if (M_tet.cells.nb() != 0) {
            Logger::out("Tet") << "Remove old tets from input mesh" 
                               << std::endl;
            M_tet.cells.clear();
            M_tet.vertices.remove_isolated();
        }
        //add new points
        index_t i;
        Logger::out("Tet") << "Add new sampled point to mesh" << std::endl;
        for (index_t v = 0; v < CVT.nb_points(); ++v) {
            if (v > nb_pts) {
                break;
            }
            i = M_tet.vertices.create_vertex();
            p = CVT.embedding(v);
            for (index_t c=0; c < 3; ++c) {
                M_tet.vertices.point(i)[c] = *p;
                p++;
            }
        }
        //tetrahedralize
        Logger::out("Tet") << "Final tetrahedralization" << std::endl;
        mesh_tetrahedralize(M_tet);
        M_tet.cells.compute_borders();
        
        if(!mesh_save(M_tet, output_filename, flags)) {
            return 1;
        }
        return 0;
    }
    
}

int main(int argc, char** argv) {
    using namespace GEO;

    
    GEO::initialize();    
    
    try {

        Stopwatch total("Total time");
        
        CmdLine::import_arg_group("standard");
        CmdLine::import_arg_group("remesh");
        CmdLine::import_arg_group("algo");
        CmdLine::import_arg_group("opt");
        
        std::vector<std::string> filenames;

        if(!CmdLine::parse(argc, argv, filenames, "inputfile <outputfile>")) {
            return 1;
        }

        
        std::string input_filename = filenames[0];
        std::string output_filename =
        filenames.size() >= 2 ? filenames[1] : std::string("out.meshb");
        Logger::out("I/O") << "Output = " << output_filename << std::endl;
        CmdLine::set_arg("input", input_filename);
        CmdLine::set_arg("output", output_filename);

        return tetrahedral_mesher(input_filename, output_filename);

    }
    catch(const std::exception& e) {
        std::cerr << "Received an exception: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}

