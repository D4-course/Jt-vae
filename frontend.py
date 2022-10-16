import json

import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Junction Tree VAE ",
    page_icon=":atom:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Junction Tree Variational Autoencoder for Molecular Graph Generation")
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Select a page", ["Home", "MolVAE", "BO", "Sampling", "MolOpt"]
)
if page == "Home":
    st.write("We seek to automate the design of molecules based on specific chemical properties. In computational terms, this task involves continuous embedding and generation of molecular graphs. Our primary contribution is the direct realization of molecular graphs, a task previously approached by generating linear SMILES strings instead of graphs. Our junction tree variational autoencoder generates molecular graphs in two phases, by first generating a tree-structured scaffold over chemical substructures, and then combining them into a molecule with a graph message passing network. This approach allows us to incrementally expand molecules while maintaining chemical validity at every step. We evaluate our model on multiple tasks ranging from molecular generation to optimization. Across these tasks, our model outperforms previous state-of-the-art baselines by a significant margin.")

                
elif page == "MolVAE":
    st.write(" Each molecule is encoded 10 times and each encoding is decoded 10 times. We report the portion of the 100 decoded molecules that are identical to the input molecule using monte carlo method.")
    smiles = st.text_input("Enter SMILES")  
    if st.button("Submit"):
        data = {"smiles": smiles}
        r = requests.post("http://localhost:5000/molvae", json=data)
        st.write(r.json())
elif page == "BO":
    st.write("Moving beyond generating valid molecules, we test how the model can produce novel molecules with desired properties. To this end, we perform Bayesian optimization in the latent space to search molecules with specified properties. Our target chemical property y(·) is octanol-water partition coefficients (logP) penalized by the synthetic accessibility (SA) score and number of long cycles.")
    seed = st.text_input("Enter seed")
    if st.button("Submit"):
        data = {"seed": seed}
        r = requests.post("http://localhost:5000/bo", json=data)
        st.write(r.text.split("\n"))
elif page == "Sampling":
    st.write("To compute validity, we sample 1000 latent vectors from the prior distribution N (0, I), and decode each of these vectors 100 times. This is the process of sampling. We output the sampled molecules in the form of SMILE strings.")
    num = st.text_input("Enter number of samples")
    if st.button("Submit"):
        r = requests.get("http://localhost:5000/sampling?num=%s" % num)
        for line in r.text.split("\n"):
            st.write(line)
elif page == "MolOpt":
    st.sidebar.header("MolOpt")
    st.sidebar.subheader("Input SMILE")
    st.sidebar.write("COc1cc2c(cc1OC)CC([NH3+])C2")
    st.sidebar.subheader("Threshold")
    st.sidebar.write("-2.50504567445")
    st.sidebar.write("For multiple inputs give ; separated values")
    st.write("The goal is to modify given molecules to improve specified properties, while constraining the degree of deviation from the original molecule. This is a more realistic scenario in drug discovery, where development of new drugs usually starts with known molecules such as existing drugs.")
    smiles = st.text_input("SMILES", value="C1=CC=CC=C1")
    st.subheader("Input Threshold")
    threshold = st.text_input("Threshold", value=0.5)
    st.subheader("Output")
    if st.button("Run"):
        data = {
            "mol": [i.strip() for i in smiles.split(";")],
            "threshold": [i.strip() for i in threshold.split(";")],
        }
        r = requests.post("http://localhost:5000/molopt", json=data)
        # make it as tables
        df = []
        t = r.text.split("\n")
        for i in range(len(t) - 2):
            temp = t[i].split("")
            print(temp)
            df.append(
                {
                    "SMILES": temp[0],
                    "Threshold": temp[1],
                    "Score": temp[2],
                    "C": temp[3],
                    "H": temp[4],
                    "N": temp[5],
                }
            )
        print(df)
        st.table(pd.DataFrame(df))
        st.write(t[-2])
