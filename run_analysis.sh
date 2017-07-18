#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_1/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_2/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_3/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_4/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_5/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_6/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_7/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_8/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_9/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_10/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_12/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8
#python /scratch/spxbp1/RBB_codes/make_splitting_dags.py -r /scratch/spxbp1/analysis_out/SNR_15/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8

#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_1/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_2/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_3/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_4/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_5/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_6/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_7/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_8/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_9/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_10/run_splitting.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_12/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_15/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_17/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_20/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_25/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_30/run_analysis.dag


#python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_1/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
#python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_2/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
#python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_3/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
#python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_4/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
#python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_5/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_6/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_7/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_8/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_9/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
python /scratch/spxbp1/RBB_codes/create_analysis_subs.py -r /scratch/spxbp1/analysis_out/SNR_10/ -S /scratch/spxbp1/RBB_codes/do_splitting.py -p /scratch/spxbp1/RBB_codes/ -N 500 -C 8 -a /scratch/spxbp1/RBB_codes/do_analysis.py
#python /scratch/spxbp1/functions_to_copy/create_analysis_subs.py -r /scratch/spxbp1/10_tests/SNR_12/ -S /scratch/spxbp1/functions_to_copy/do_splitting.py -p /scratch/spxbp1/functions_to_copy/ -N 10 -C 8 -a /scratch/spxbp1/functions_to_copy/do_analysis.py
#python /scratch/spxbp1/functions_to_copy/create_analysis_subs.py -r /scratch/spxbp1/10_tests/SNR_15/ -S /scratch/spxbp1/functions_to_copy/do_splitting.py -p /scratch/spxbp1/functions_to_copy/ -N 10 -C 8 -a /scratch/spxbp1/functions_to_copy/do_analysis.py
#python /scratch/spxbp1/functions_to_copy/create_analysis_subs.py -r /scratch/spxbp1/10_tests/SNR_17/ -S /scratch/spxbp1/functions_to_copy/do_splitting.py -p /scratch/spxbp1/functions_to_copy/ -N 10 -C 8 -a /scratch/spxbp1/functions_to_copy/do_analysis.py
#python /scratch/spxbp1/functions_to_copy/create_analysis_subs.py -r /scratch/spxbp1/10_tests/SNR_20/ -S /scratch/spxbp1/functions_to_copy/do_splitting.py -p /scratch/spxbp1/functions_to_copy/ -N 10 -C 8 -a /scratch/spxbp1/functions_to_copy/do_analysis.py
#python /scratch/spxbp1/functions_to_copy/create_analysis_subs.py -r /scratch/spxbp1/10_tests/SNR_25/ -S /scratch/spxbp1/functions_to_copy/do_splitting.py -p /scratch/spxbp1/functions_to_copy/ -N 10 -C 8 -a /scratch/spxbp1/functions_to_copy/do_analysis.py
#python /scratch/spxbp1/functions_to_copy/create_analysis_subs.py -r /scratch/spxbp1/10_tests/SNR_30/ -S /scratch/spxbp1/functions_to_copy/do_splitting.py -p /scratch/spxbp1/functions_to_copy/ -N 10 -C 8 -a /scratch/spxbp1/functions_to_copy/do_analysis.py
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_1/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_2/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_3/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_4/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_5/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_6/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_7/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_8/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_9/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_10/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_12/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_15/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_17/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_20/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_25/run_analysis.dag
#condor_submit_dag /scratch/spxbp1/analysis_out/SNR_30/run_analysis.dag


