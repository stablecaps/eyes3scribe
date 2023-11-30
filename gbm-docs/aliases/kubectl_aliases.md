
kubectl aliases
===============


***(in /home/bsgt/stablecaps_bashrc/aliases/kubectl_aliases.sh)***
## Aliases


| **Alias Name** | **Code** | **Notes** |
| ------------- | ------------- | ------------- |
| **kc** | `kubectl` | 
| **kcgp** | `kubectl get pods` | 
| **kcgd** | `kubectl get deployments` | 
| **kcgn** | `kubectl get nodes` | 
| **kcdp** | `kubectl describe pod` | 
| **kcdd** | `kubectl describe deployment` | 
| **kcdn** | `kubectl describe node` | 
| **kcgpan** | `kubectl get pods --all-namespaces` | 
| **kcgdan** | `kubectl get deployments --all-namespaces` | 
| **kcnetshoot** | `kubectl run --generator=run-pod/v1 netshoot-$(date +%s) --rm -i --tty --image nicolaka/netshoot -- /bin/bash` | 
