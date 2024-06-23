from datetime import datetime
import dd_content

class DailyDigestEmail:
    def __init__(self) -> None:
        self.content = {
            "quote": {"include": True, "content": dd_content.get_random_quote()},
            "weather": {"include": True, "content": dd_content.get_weather_forecast()},
            "wikipedia": {"include": True, "content": dd_content.get_wikipedia_article()}
        }

    def format_message(self):
        #### Generate Plain Text Message #####
        ######################################
        current_date = datetime.now().strftime("%d %b %Y")
        text_msg = ""
        ## heading first
        text_msg += f"**** Welcome to daily digest {current_date} *****"
        text_msg += "\n"
        ## Get Random Quote ######
        if self.content["quote"]["include"] and self.content["quote"]["content"]:
            text_msg += f"\t*** Quote of the Day *****\n\t{self.content['quote']['content']['quote']} - {self.content['quote']['content']['author']}"
            text_msg += "\n"
        ## Get Weather forecast
        if self.content["weather"]["include"] and self.content["weather"]["content"]:
            text_msg += f"\t*** Weather forecast for {self.content['weather']['content']['city']},{self.content['weather']['content']['country']} {current_date} *****\n"
            ## Loop over each period 
            for each_forecast in self.content["weather"]["content"]["periods"]:
                  text_msg +=f"{each_forecast['timestamp'].strftime('%d %b %H%M')} - {each_forecast['temp']}\u00B0C | {each_forecast['description']}\n"

            text_msg += "\n"
        
        if self.content["wikipedia"]["include"] and self.content["wikipedia"]["content"]:
            text_msg += f"\t**** Daily Random Learning *****\n\n"
            text_msg += f"{self.content['wikipedia']['content']['title']}\n{self.content['wikipedia']['content']['extract']}"
            text_msg += "\n"

        ### Generate HTML Message ###########
        ####################################
        html = f"""<html>
            <body>
    <center>
        <h1>Daily Digest - {current_date}</h1>
        """

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            html += f"""
        <h2>Quote of the Day</h2>
        <i>"{self.content['quote']['content']['quote']}"</i> - {self.content['quote']['content']['author']}
        """

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            html += f"""
        <h2>Forecast for {self.content['weather']['content']['city']}, {self.content['weather']['content']['country']}</h2> 
        <table>
                    """

            for forecast in self.content['weather']['content']['periods']:
                html += f"""
            <tr>
                <td>
                    {forecast['timestamp'].strftime('%d %b %H%M')}
                </td>
                <td>
                    <img src="{forecast['icon']}">
                </td>
                <td>
                    {forecast['temp']}\u00B0C | {forecast['description']}
                </td>
            </tr>
                        """               

            html += """
            </table>
                    """
        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            html += f"""
        <h2>Daily Random Learning</h2>
        <h3><a href="{self.content['wikipedia']['content']['url']}">{self.content['wikipedia']['content']['title']}</a></h3>
        <table width="800">
            <tr>
                <td>{self.content['wikipedia']['content']['extract']}</td>
            </tr>
        </table>
                    """

        # footer
        html += """
    </center>
    </body>
        </html>
        """
        return {'text': text_msg, 'html': html}


    def send_email():
        pass 



if __name__ == "__main__":
    ## printing text message ##
    formatted_msg = DailyDigestEmail().format_message()
    # print(formatted_msg)
    # print Plaintext and HTML messages
    print('\nPlaintext email body is...')
    print(formatted_msg['text'])
    print('\n------------------------------------------------------------')
    print('\nHTML email body is...')
    print(formatted_msg['html'])

    # save Plaintext and HTML messages to file
    with open('message_text.txt', 'w', encoding='utf-8') as f:
        f.write(formatted_msg['text'])
    with open('message_html.html', 'w', encoding='utf-8') as f:
        f.write(formatted_msg['html'])