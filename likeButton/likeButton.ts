interface Item {
    item_id: string;
    item_name: string;
    item_likes: ItemLike[];
}

interface ItemLikes {
    like_id: string;
    liker_account_id: string;
    item_id: string;
}
class ItemLike extends UIController {
    @State()
    private accountId: string;

    @State()
    private items: Item[];

    protected BindRouterParams() {
        const session_id = Services.StateService.GetSessionId();
        BrokerClient.GetSessionInfo(session_id).then(sessionInfo => {
            this.accountId = sessionInfo.account_id
        }
        BrokerClient.GetItemList().then((results) => {
            this.items = results
        })
    }

    private likeOrUnlikeItems(item_id: string) {
        BrokerClient.LikeOrUnlikeItem(item_id).then(()=> console.log("Başarılı"))
    }

    private showLikes(likes: IGetLikes[]) {
        if (likes != null) {
            return likes.find(o => o.liker_account_id == this.accountId)
        }
        else {
            return false
        }
    }

    public LoadView() {
        return(
            VStack(
                ...ForEach(this.items)(item => 
                    this.showLikes(item.item_likes) ?
                    Text("Unlike").onClick(()=> this.likeOrUnlikeItems(item.item_id))
                     :
                    Text("Like").onClick(()=> this.likeOrUnlikeItems(item.item_id))
                    )
                
            )
        )
    }


}