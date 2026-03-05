import argparse

args = None

def init_parser():
    global args
    parser = argparse.ArgumentParser(description="Pipeline de Analítica para RPA")
    parser.add_argument(
        '--mode', 
        type=str, 
        choices=['DEV', 'PROD'], 
        default='DEV', 
        help="Entorno de ejecución"
    )
    args = parser.parse_args()
    
    return args