from flask import Flask, request, jsonify
import os
class ConfigMessage:
    def __init__(self, log_level, grpc_port, environment, db_url):
        self.log_level = log_level
        self.grpc_port = grpc_port
        self.environment = environment
        self.db_url = db_url

class DomainMessage:
    def __init__(self, endpoint, domain, log_level):
        self.endpoint = endpoint
        self.domain = domain
        self.log_level = log_level

class LoadCapabilityMessage:
    def __init__(self, cpu, memory):
        self.cpus = cpu
        self.memorys = memory

app = Flask(__name__)

def get_env_variable(key, default_value):
    return os.environ.get(key, default_value)

@app.route('/config')
def get_config():
    log_level = get_env_variable('LOG_LEVEL', 'debug')
    grpc_port = get_env_variable('GRPC_PORT', '8080')
    environment = get_env_variable('ENVIRONMENT', 'dev')
    db_url = get_env_variable('DB_URL', 'postgres://admin:supersecret@10.10.10.1:5432/exam-db')

    message = ConfigMessage(log_level, grpc_port, environment, db_url)
    return jsonify(message.__dict__)

@app.route('/domain')
def get_domain():
    host = request.host
    print(f'Host: {host}')

    log_level = get_env_variable('LOG_LEVEL', 'debug')
    message = DomainMessage('/domain', host, log_level)
    return jsonify(message.__dict__)

@app.route('/load-capability')
def get_load():
    cpu_limit = get_env_variable('CPU', '0.1')
    memory_limit = get_env_variable('MEMORY', '32Mi')

    message = LoadCapabilityMessage(cpu_limit, memory_limit)
    return jsonify(message.__dict__)

if __name__ == '__main__':
    port = 8080
    app.run(port=port, debug=True)
