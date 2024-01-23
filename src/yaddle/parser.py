import pandas as pd


class Parser:
    
    def __init__(
        self,
        filename: str
    ):
        with open(filename) as infile:
            self._raw_data = infile.readlines()
        
        self.results = {}

    def parse(self):
        
        final_result = {}
        
        _in_data_block = False
        _in_meta_block = False
        _in_summary_block = False
        _seen_summary = False
        _in_results_block = False
        
        metadata = {}
        
        _summary = []
        _summary_titles = None
        summary_df = None
        
        _results_titles = None
        _results = []
        results_df = None
        
        for i, row in enumerate(self._raw_data):
            
            if not row:
                continue
            
            if not _in_data_block and row.startswith("BEGIN"):
                _in_data_block = True
                
                metadata['something'] = row.split()[1]
                _in_meta_block = True
                continue
            
            if _in_meta_block and not row.startswith('-'):
                try:
                    field, data = row.split()
                    # Break out at the end of the file
                    if field == 'Type:' and data.strip() != 'Profile1D':
                        break
                    
                except ValueError:
                    field = row
                    data = ''
                metadata[field.replace(":", "")] = data
                continue
            
            elif _in_meta_block and row.startswith('-'):
                _in_meta_block = False
                continue
            
            if (row.startswith('#') 
                and not _in_summary_block 
                and not _in_results_block
            ):
                _in_summary_block = True
                _summary_titles = row.split('\t')[1:]
                continue
            
            elif _in_summary_block and not row.startswith('#'):
                _row = row.split('\t')[1:]
                _row = [row[0]] + [float(item) for item in _row[1:]]
                _summary.append(_row)
                continue
            
            elif _in_summary_block and row.startswith('#'):
                # Build our summary df now, as we're breaking out
                summary_df = pd.DataFrame(_summary, columns=_summary_titles)
                _in_summary_block = False
                _seen_summary = True
                
            if _seen_summary and row.startswith('#'):
                _in_results_block = True
                _results_titles = row.split('\t')
                _results_titles[0] = _results_titles[0].replace('# ', '')
                continue
            
            elif _in_results_block and not row.startswith('END'):
                _results.append([float(item) for item in row.split('\t')])
                continue
            
            elif row.startswith('END'):
                results_df = pd.DataFrame(_results, columns=_results_titles)
                
                name = metadata['Path']
                
                final_result[name] = {
                    'metadata': metadata,
                    'summary': summary_df,
                    'results': results_df
                }
                
                # Reset everything
                _in_data_block = False
                _in_meta_block = False
                _in_summary_block = False
                _seen_summary = False
                _in_results_block = False
                
                metadata = {}
                
                _summary = []
                _summary_titles = None
                summary_df = None
                
                _results_titles = None
                _results = []
                results_df = None
                
        return final_result
                
                
            
                
                
                