import argparse

nginx_server_script = '''upstream fastapi {
{FASTAPI_SERVERS}
}

server {
    listen {DOMAIN_PORT};
    server_name {DOMAIN_ADDR};

    location / {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='script to create nginx load balancing essentials')
    parser.add_argument('--fa_addr', type=str, default="0.0.0.0", help='fastapi server address')
    parser.add_argument('--fa_ports', type=str, default="8001, 8002", help='comma separated fastapi server ports')
    parser.add_argument('--master_addr', type=str, default="0.0.0.0", help='master address')
    parser.add_argument('--master_port', type=str, default="80", help='master port')
    parser.add_argument('--nginx_script_filename', type=str, default='fastapi_loadbalancer', help='filename for nginx script')
    args = parser.parse_args()

    fa_ports = list([port.strip() for port in str(args.fa_ports).split(",")])
    fa_servers = "\n".join([f"    server {str(args.fa_addr)}:{fa_port};" for fa_port in fa_ports])
    fa_servers_command = "\n".join( [
        f"uvicorn embedding_model_server:app --host 0.0.0.0 --port {fa_port}"
        for fa_port in fa_ports
    ] )
    
    nss_filedata = nginx_server_script.\
        replace("{FASTAPI_SERVERS}", fa_servers).\
        replace("{DOMAIN_ADDR}", str(args.master_addr)).\
        replace("{DOMAIN_PORT}", str(args.master_port))
    nginx_filename = str(args.nginx_script_filename)
    with open(nginx_filename, "w") as filepointer:
        filepointer.write(nss_filedata)
    
    print(f'''
!!!! PLEASE EXECUTE THE COMMANDS BELOW TO SETUP FASTAPI SERVER AND LOADBALANCER !!!!
```
{fa_servers_command}
cp -r {nginx_filename} /etc/nginx/sites-available/{nginx_filename}
sudo ln -s /etc/nginx/sites-available/{nginx_filename} /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
    ''')

