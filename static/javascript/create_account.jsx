class createAccount extends React.Component {
    constructor(props) {
    super(props);

        this.state = {
        username: '',
        password: '',
        email: '',
        }

        this.handleChange = this.handleChange.bind(this);
        this.hangleChange = this.handleSubmit.bind(this);
        this.componentDidUpdate = this.componentDidUpdate.bind(this);

        }

}