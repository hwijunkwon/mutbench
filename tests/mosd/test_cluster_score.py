import json, subprocess, tempfile, os

def test_cluster_score_cli():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("sample,label\ns1,0\ns2,0\ns3,1\ns4,1\n")
        true_path = f.name
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("sample,label\ns1,0\ns2,0\ns3,1\ns4,1\n")
        pred_path = f.name
    try:
        result = subprocess.run(
            ['python', '-m', 'tools.mosd.cluster_score', '--true', true_path, '--pred', pred_path, '--format', 'json'],
            capture_output=True, text=True, cwd='/proj/paper'
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        assert data['cluster_score'] == 1.0
    finally:
        os.unlink(true_path)
        os.unlink(pred_path)
