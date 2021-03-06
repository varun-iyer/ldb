from app import app, db
from app.models import Document, reference
from app.ref import get_doc, build_graph
from networkx.drawing.nx_pydot import write_dot

@app.shell_context_processor
def make_shell_context():
    return {
            'db': db,
            'Document': Document,
            'reference':reference,
            'get_doc':get_doc,
            'build_graph':build_graph,
            'write_dot':write_dot
        }
